#!/usr/bin/env python3
r"""Reverse-sync: fragmen LaTeX (.tex) -> bab Quarto (.qmd) untuk website.

Dipakai saat naskah utama disunting di LaTeX dan website perlu ikut update.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

OUT_ROOT = Path(__file__).resolve().parents[1]
ROOT = OUT_ROOT.parent
CH_DIR = OUT_ROOT / "chapters"
FIGSRC_DIR = OUT_ROOT / "figures" / "_src"
QMD_DIR = ROOT / "website" / "chapters"
WEB_FIG_DIR = ROOT / "website" / "figures"

BODY_MARK = "% >>>>> ISI OTOMATIS (jangan hapus baris ini) >>>>>"
FIG_RE = re.compile(r"\\begin\{figure\}.*?\\end\{figure\}", re.S)
IMG_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")
CAP_RE = re.compile(r"\\caption\{(.*?)\}\s*$", re.S | re.M)


def get_body(tex_path: Path) -> str:
    text = tex_path.read_text(encoding="utf-8")
    return text.split(BODY_MARK + "\n", 1)[1] if BODY_MARK + "\n" in text else text


def strip_balanced(text: str, macro: str, keep: int) -> str:
    r"""Remove \macro{..}{..} while retaining the selected argument."""
    output, index, tag = [], 0, "\\" + macro
    while index < len(text):
        start = text.find(tag, index)
        if start < 0:
            output.append(text[index:])
            break
        output.append(text[index:start])
        cursor = start + len(tag)
        arguments = []
        while cursor < len(text) and text[cursor] == "{":
            depth, argument_start = 0, cursor
            while cursor < len(text):
                if text[cursor] == "{":
                    depth += 1
                elif text[cursor] == "}":
                    depth -= 1
                    if depth == 0:
                        cursor += 1
                        break
                cursor += 1
            arguments.append(text[argument_start + 1 : cursor - 1])
        output.append(arguments[keep] if keep < len(arguments) else "")
        index = cursor
    return "".join(output)


def preclean(tex: str) -> str:
    tex = strip_balanced(tex, "texorpdfstring", 0)
    tex = strip_balanced(tex, "passthrough", 0)
    tex = re.sub(r"\\label\{[^}]*\}", "", tex)
    tex = re.sub(r"\\tightlist\s*", "", tex)
    # The print layout wraps generated tables in a local group with commands
    # that Pandoc's LaTeX reader does not support. Keep the surrounding prose
    # and replace the print-only table block with an explicit web notice.
    tex = re.sub(
        r"\{\\def\\LTcaptype\{none\}.*?\n\}\n",
        lambda _match: "\n\\emph{Tabel lengkap tersedia pada edisi cetak.}\n",
        tex,
        flags=re.S,
    )
    tex = re.sub(r"\\tabeljudul\{(.*?)\}", r"\\textbf{\1}", tex, flags=re.S)
    for environment in ("pendalaman", "sintesis", "bacaan", "CSLReferences"):
        tex = re.sub(rf"^\\begin\{{{environment}\}}.*$", "", tex, flags=re.M)
        tex = tex.replace(rf"\end{{{environment}}}", "")
    tex = re.sub(r"\\rujukanheading", "", tex)
    tex = re.sub(r"\\bibitem(?:\[[^\]]*\])?\{[^}]*\}", "", tex)
    return tex


def mermaid_block(source: list[str]) -> str:
    return "```{mermaid}\n" + "\n".join(source) + "\n```"


def restore_figures(tex: str, stem: str) -> tuple[str, dict[str, str]]:
    """Replace figures with tokens, then map each token to its Quarto form."""
    sidecar_path = FIGSRC_DIR / f"{stem}.json"
    sidecar = json.loads(sidecar_path.read_text(encoding="utf-8")) if sidecar_path.exists() else {}
    replacements: dict[str, str] = {}

    def substitute(match: re.Match[str]) -> str:
        environment = match.group(0)
        image_match = IMG_RE.search(environment)
        image_path = image_match.group(1) if image_match else ""
        image_name = os.path.basename(image_path)
        image_stem, image_extension = os.path.splitext(image_name)
        token = f"XXFIGURE{len(replacements):03d}XX"
        if image_stem in sidecar:
            replacements[token] = mermaid_block(sidecar[image_stem]["src"])
        else:
            caption_match = CAP_RE.search(environment)
            caption = caption_match.group(1).strip() if caption_match else ""
            if image_extension:
                extension = image_extension
            else:
                extension = next(
                    (
                        candidate
                        for candidate in (".png", ".jpg", ".jpeg", ".pdf")
                        if (OUT_ROOT / "figures" / f"{image_stem}{candidate}").exists()
                    ),
                    ".png",
                )
            source_path = OUT_ROOT / "figures" / f"{image_stem}{extension}"
            WEB_FIG_DIR.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, WEB_FIG_DIR / source_path.name)
            replacements[token] = f"![{caption}](../figures/{source_path.name})"
        return "\n\n" + token + "\n\n"

    return FIG_RE.sub(substitute, tex), replacements


def run_pandoc(tex: str) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".tex", delete=False, encoding="utf-8") as file:
        file.write(tex)
        temporary_path = file.name
    try:
        result = subprocess.run(
            [
                "quarto",
                "pandoc",
                temporary_path,
                "-f",
                "latex",
                "-t",
                "markdown",
                "--wrap=preserve",
                "--markdown-headings=atx",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr)
        return result.stdout
    finally:
        os.unlink(temporary_path)


def postclean(markdown: str) -> str:
    markdown = re.sub(r"^(#+ .*?)\s*\{#[^}]*\}\s*$", r"\1", markdown, flags=re.M)
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    return markdown.strip() + "\n"


def reverse_chapter(stem: str) -> None:
    tex_path = CH_DIR / f"{stem}.tex"
    if not tex_path.exists():
        print(f"  {stem}: .tex tidak ada, dilewati")
        return
    body, replacements = restore_figures(get_body(tex_path), stem)
    markdown = run_pandoc(preclean(body))
    for token, block in replacements.items():
        markdown = re.sub(r"^\s*" + token + r"\s*$", lambda _match, value=block: value, markdown, flags=re.M)
    markdown = postclean(markdown)
    (QMD_DIR / f"{stem}.qmd").write_text(markdown, encoding="utf-8")
    print(f"  {stem}: {len(replacements)} gambar dipulihkan, {len(markdown.splitlines())} baris qmd")


def main() -> None:
    stems = [argument for argument in sys.argv[1:] if not argument.startswith("-")] or [f"ch{number:02d}" for number in range(1, 18)]
    print(f"Reverse-sync {len(stems)} bab: .tex -> .qmd")
    for stem in stems:
        reverse_chapter(stem)
    print("Selesai.")


if __name__ == "__main__":
    main()
