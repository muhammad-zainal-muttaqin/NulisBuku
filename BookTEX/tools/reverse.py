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
WEB_INDEX = ROOT / "website" / "index.qmd"
WEB_CONFIG = ROOT / "website" / "_quarto.yml"

BODY_MARK = "% >>>>> ISI OTOMATIS (jangan hapus baris ini) >>>>>"
FIG_RE = re.compile(r"\\begin\{figure\}.*?\\end\{figure\}", re.S)
IMG_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")
CAP_RE = re.compile(r"\\caption\{(.*?)\}\s*$", re.S | re.M)
TABLE_RE = re.compile(
    r"\\tabeljudul\{(?P<title>.*?)\}\s*"
    r"\{\\def\\LTcaptype\{none\}.*?"
    r"\\begin\{xltabular\}.*?\n(?P<body>.*?)"
    r"\\end\{xltabular\}.*?\n\s*\}",
    re.S,
)
TABLE_GROUP_RE = re.compile(
    r"\{\\def\\LTcaptype\{none\}.*?"
    r"\\begin\{xltabular\}.*?\n(?P<body>.*?)"
    r"\\end\{xltabular\}.*?\n\s*\}",
    re.S,
)


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
    tex = re.sub(r"\\bibitem(?:\[[^\]]*\])?\{[^}]*\}", "", tex)
    return tex


def clean_table_cell(cell: str) -> str:
    """Convert the limited LaTeX used inside generated table cells to Markdown."""
    math_fragments: list[str] = []

    def protect_math(match: re.Match[str]) -> str:
        token = f"XXMATH{len(math_fragments):03d}XX"
        math_fragments.append(f"${match.group(1).strip()}$")
        return token

    # Clean surrounding LaTeX without stripping commands such as \text{} from math.
    cell = re.sub(r"\\\((.*?)\\\)", protect_math, cell)
    cell = re.sub(r"\\(?:toprule|midrule|bottomrule|endhead)\b", "", cell)
    cell = re.sub(r"\\(?:emph|textit)\{([^{}]*)\}", r"*\1*", cell)
    cell = re.sub(r"\\textbf\{([^{}]*)\}", r"**\1**", cell)
    cell = re.sub(r"\\(?:texttt|seqsplit)\{([^{}]*)\}", r"`\1`", cell)
    cell = re.sub(r"\\passthrough\{\\lstinline!([^!]*)!\}", r"`\1`", cell)
    cell = cell.replace(r"\_", "_").replace(r"\&", "&")
    cell = cell.replace(r"\ ", " ")
    cell = re.sub(r"\\[a-zA-Z]+(?:\[[^\]]*\])?", "", cell)
    cell = cell.replace("{", "").replace("}", "")
    for index, fragment in enumerate(math_fragments):
        cell = cell.replace(f"XXMATH{index:03d}XX", fragment)
    return " ".join(cell.split()).replace("|", r"\|")


def table_block(title: str, body: str, identifier: str) -> str:
    title = clean_table_cell(title.replace("---", "—"))
    caption = re.sub(r"^Tabel\s+\d+(?:\.\d+)?\s+[—-]+\s*", "", title)
    rows = []
    for raw_row in re.split(r"\\\\", body):
        raw_row = raw_row.strip()
        if not raw_row or raw_row.startswith(r"\bottomrule"):
            continue
        cells = [clean_table_cell(cell) for cell in raw_row.split("&")]
        if any(cells):
            rows.append(cells)
    if len(rows) < 2:
        raise ValueError(f"Tidak dapat mengonversi tabel: {title}")
    width = max(len(row) for row in rows)
    rows = [row + [""] * (width - len(row)) for row in rows]
    header, data = rows[0], rows[1:]
    lines = ["::: {.tabel-buku}", "", "| " + " | ".join(header) + " |", "| " + " | ".join(["---"] * width) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in data)
    lines.extend(["", f": {caption} {{#{identifier}}}", "", ":::"])
    return "\n".join(lines)


def replace_tables(tex: str, stem: str, blocks: dict[str, str]) -> str:
    """Convert every print-table block associated with a tabeljudul command."""
    marker, cursor, output = r"\tabeljudul", 0, []
    while True:
        start = tex.find(marker, cursor)
        if start < 0:
            output.append(tex[cursor:])
            return "".join(output)
        output.append(tex[cursor:start])
        title_start = start + len(marker)
        if title_start >= len(tex) or tex[title_start] != "{":
            raise ValueError("Judul tabel tidak memiliki argumen")
        title_end = find_closing_brace(tex, title_start)
        title = tex[title_start + 1 : title_end]
        next_title = tex.find(marker, title_end + 1)
        segment_end = next_title if next_title >= 0 else len(tex)
        segment = tex[title_end + 1 : segment_end]
        table_matches = list(TABLE_GROUP_RE.finditer(segment))
        if not table_matches:
            output.append(tex[start:segment_end])
            cursor = segment_end
            continue
        segment_cursor = 0
        for index, match in enumerate(table_matches, start=1):
            output.append(segment[segment_cursor : match.start()])
            table_number = len([key for key in blocks if key.startswith("XXBLOCK")]) + 1
            token = f"XXBLOCK{len(blocks):03d}XX"
            caption = title if index == 1 else f"{title} (lanjutan)"
            blocks[token] = table_block(caption, match.group("body"), f"tbl-{stem}-{table_number}") + "\n"
            output.append(f"\n\n{token}\n\n")
            segment_cursor = match.end()
        output.append(segment[segment_cursor:])
        cursor = segment_end


def find_closing_brace(text: str, start: int) -> int:
    """Return the closing brace paired with text[start]."""
    depth = 0
    for index in range(start, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return index
    raise ValueError("Kurung kurawal LaTeX tidak seimbang")


def convert_fragment(tex: str) -> str:
    return postclean(run_pandoc(preclean(tex))).strip()


def extract_environment(
    tex: str,
    environment: str,
    blocks: dict[str, str],
    render,
    titled: bool = False,
) -> str:
    """Replace one kind of LaTeX environment with Quarto block tokens."""
    begin, end, cursor, output = rf"\begin{{{environment}}}", rf"\end{{{environment}}}", 0, []
    while True:
        start = tex.find(begin, cursor)
        if start < 0:
            output.append(tex[cursor:])
            return "".join(output)
        output.append(tex[cursor:start])
        content_start, title = start + len(begin), ""
        if titled:
            if content_start >= len(tex) or tex[content_start] != "{":
                raise ValueError(f"Judul {environment} tidak ditemukan")
            title_end = find_closing_brace(tex, content_start)
            title = tex[content_start + 1 : title_end]
            content_start = title_end + 1
        elif environment == "CSLReferences":
            for _ in range(2):
                if content_start < len(tex) and tex[content_start] == "{":
                    content_start = find_closing_brace(tex, content_start) + 1
        end_start = tex.find(end, content_start)
        if end_start < 0:
            raise ValueError(f"Penutup {environment} tidak ditemukan")
        token = f"XXBLOCK{len(blocks):03d}XX"
        blocks[token] = render(title, convert_fragment(tex[content_start:end_start]))
        output.append(f"\n\n{token}\n\n")
        cursor = end_start + len(end)


def mermaid_block(source: list[str]) -> str:
    return "```{mermaid}\n" + "\n".join(source) + "\n```"


def pendalaman_block(title: str, content: str) -> str:
    title = convert_fragment(title)
    return (
        "::: {.pendalaman}\n"
        "<div class=\"pendalaman-label\">Pendalaman</div>\n\n"
        f"### {title} {{.pendalaman-title .unnumbered .unlisted}}\n\n"
        f"{content}\n"
        ":::\n"
    )


def sintesis_block(_title: str, content: str) -> str:
    return (
        "::: {.sintesis-bab}\n\n"
        "## Sintesis Bab {.unnumbered .unlisted}\n\n"
        f"{content}\n"
        ":::\n"
    )


def bacaan_block(_title: str, content: str) -> str:
    return f"## Bacaan Lanjutan {{.bacaan-lanjutan .unnumbered .unlisted}}\n\n{content}\n"


def rujukan_block(_title: str, content: str) -> str:
    return f"::: {{.references}}\n\n{content}\n\n:::\n"


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
            caption = clean_table_cell(caption_match.group(1).strip()) if caption_match else ""
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
            replacements[token] = f"![{caption}](../figures/{source_path.name}){{#fig-{image_stem}}}"
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
    blocks: dict[str, str] = {}
    body = extract_environment(body, "pendalaman", blocks, pendalaman_block, titled=True)
    body = extract_environment(body, "sintesis", blocks, sintesis_block)
    body = extract_environment(body, "bacaan", blocks, bacaan_block)
    body = extract_environment(body, "CSLReferences", blocks, rujukan_block)

    rujukan_token = f"XXBLOCK{len(blocks):03d}XX"
    blocks[rujukan_token] = "## Rujukan {.rujukan .unnumbered .unlisted}"
    body = body.replace(r"\rujukanheading", f"\n\n{rujukan_token}\n\n")

    # Pandoc cannot read the print-specific xltabular wrapper, so preserve
    # tables as Quarto-native Markdown before converting the surrounding prose.
    body = replace_tables(body, stem, blocks)
    markdown = convert_fragment(body)
    for token, block in replacements.items():
        markdown = re.sub(
            r"^[ \t]*" + token + r"[ \t]*$",
            lambda _match, value=block: f"\n\n{value}\n\n",
            markdown,
            flags=re.M,
        )
    for token, block in blocks.items():
        markdown = re.sub(
            r"^[ \t]*" + token + r"[ \t]*$",
            lambda _match, value=block: f"\n\n{value}\n\n",
            markdown,
            flags=re.M,
        )
    markdown = postclean(markdown)
    (QMD_DIR / f"{stem}.qmd").write_text(markdown, encoding="utf-8")
    print(f"  {stem}: {len(replacements)} gambar dipulihkan, {len(markdown.splitlines())} baris qmd")


def reverse_front_matter() -> None:
    """Sync the website title, authors, and preface from the LaTeX source."""
    metadata = (OUT_ROOT / "metadata.tex").read_text(encoding="utf-8")
    title_match = re.search(r"\\title\{([^}]*)\}", metadata)
    author_match = re.search(r"\\author\{(.*?)\}", metadata, re.S)
    if not title_match or not author_match:
        raise ValueError("Metadata buku tidak lengkap")
    title = clean_table_cell(title_match.group(1))
    authors = [clean_table_cell(author) for author in author_match.group(1).split(r"\and")]

    config = WEB_CONFIG.read_text(encoding="utf-8")
    config = re.sub(r'(?m)^  title: ".*"$', f'  title: "{title}"', config)
    config = re.sub(
        r'(?m)^  author:.*(?:\n    - .*?)*(?=\n  [a-z]|\n\w|\Z)',
        "  author:\n" + "\n".join(f"    - \"{author}\"" for author in authors),
        config,
    )
    WEB_CONFIG.write_text(config, encoding="utf-8")

    preface = (OUT_ROOT / "prakata.tex").read_text(encoding="utf-8")
    start = preface.find(r"\markboth{Prakata}{}")
    end = preface.rfind(r"\endgroup")
    if start < 0 or end < 0:
        raise ValueError("Isi prakata tidak ditemukan")
    content = convert_fragment(preface[start + len(r"\markboth{Prakata}{}") : end])
    content = content.replace("::: flushright", "::: {.text-end}")
    WEB_INDEX.write_text(f"# Prakata {{.unnumbered}}\n\n{content}", encoding="utf-8")
    print("  Front matter: metadata dan prakata disinkronkan")


def main() -> None:
    stems = [argument for argument in sys.argv[1:] if not argument.startswith("-")] or [f"ch{number:02d}" for number in range(1, 18)]
    print(f"Reverse-sync {len(stems)} bab: .tex -> .qmd")
    reverse_front_matter()
    for stem in stems:
        reverse_chapter(stem)
    print("Selesai.")


if __name__ == "__main__":
    main()
