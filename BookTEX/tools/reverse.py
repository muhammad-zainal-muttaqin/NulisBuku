#!/usr/bin/env python3
r"""Reverse-sync: fragmen LaTeX (.tex) -> bab Quarto (.qmd) untuk website.

Dipakai saat naskah utama disunting di LaTeX dan website perlu ikut update.
Alur per bab:
  1. Ambil isi .tex (setelah penanda BODY_MARK).
  2. Ganti tiap environment figure -> token; nanti dikembalikan jadi blok
     ```{mermaid} hidup dari sidecar figures/_src/chNN.json (kunci = nama gambar).
     Kalau gambar tak ada di sidecar (mis. gambar baru buatan tangan), pakai
     ![caption](figures/chNN-fig-K.png) sebagai fallback.
  3. Bersihkan makro khusus pandoc (\passthrough, \tightlist, \texorpdfstring,
     \label) agar bisa dibaca ulang.
  4. pandoc latex -> markdown.
  5. Sisipkan kembali blok mermaid, rapikan, tulis website/chapters/chNN.qmd.

Pemakaian:
  python tools/reverse.py            # semua bab
  python tools/reverse.py ch16       # bab tertentu
"""
from __future__ import annotations
import json, os, re, subprocess, sys, tempfile
from pathlib import Path

OUT_ROOT   = Path(__file__).resolve().parents[1]          # .../BookTEX
ROOT       = OUT_ROOT.parent                              # .../NulisBuku
CH_DIR     = OUT_ROOT / "chapters"
FIGSRC_DIR = OUT_ROOT / "figures" / "_src"
QMD_DIR    = ROOT / "website" / "chapters"

BODY_MARK  = "% >>>>> ISI OTOMATIS (jangan hapus baris ini) >>>>>"
FIG_RE     = re.compile(r"\\begin\{figure\}.*?\\end\{figure\}", re.S)
IMG_RE     = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")
CAP_RE     = re.compile(r"\\caption\{(.*?)\}\s*$", re.S | re.M)


def get_body(tex_path: Path) -> str:
    txt = tex_path.read_text(encoding="utf-8")
    return txt.split(BODY_MARK + "\n", 1)[1] if BODY_MARK + "\n" in txt else txt


def strip_balanced(s: str, macro: str, keep: int) -> str:
    r"""Hapus \macro{..}{..} dan pertahankan argumen ke-'keep' (0-based)."""
    out, i, tag = [], 0, "\\" + macro
    while i < len(s):
        j = s.find(tag, i)
        if j < 0:
            out.append(s[i:]); break
        out.append(s[i:j])
        k = j + len(tag)
        args = []
        while k < len(s) and s[k] == "{":
            depth, start = 0, k
            while k < len(s):
                if s[k] == "{": depth += 1
                elif s[k] == "}":
                    depth -= 1
                    if depth == 0: k += 1; break
                k += 1
            args.append(s[start + 1:k - 1])
        out.append(args[keep] if keep < len(args) else "")
        i = k
    return "".join(out)


def preclean(tex: str) -> str:
    tex = strip_balanced(tex, "texorpdfstring", 0)   # simpan versi TeX
    tex = strip_balanced(tex, "passthrough", 0)
    tex = re.sub(r"\\label\{[^}]*\}", "", tex)
    tex = re.sub(r"\\tightlist\s*", "", tex)
    return tex


def mermaid_block(src: list[str]) -> str:
    return "```{mermaid}\n" + "\n".join(src) + "\n```"


def restore_figures(tex: str, stem: str) -> tuple[str, dict[str, str]]:
    """Ganti tiap figure -> token unik. Kembalikan (tex_baru, {token: blok_pengganti})."""
    sc_path = FIGSRC_DIR / f"{stem}.json"
    sidecar = json.loads(sc_path.read_text(encoding="utf-8")) if sc_path.exists() else {}
    repl: dict[str, str] = {}

    def sub(m: re.Match) -> str:
        env = m.group(0)
        img_m = IMG_RE.search(env)
        img = img_m.group(1) if img_m else ""
        img = os.path.splitext(os.path.basename(img))[0]
        token = f"XXFIGURE{len(repl):03d}XX"
        if img in sidecar:
            repl[token] = mermaid_block(sidecar[img]["src"])
        else:
            cap_m = CAP_RE.search(env)
            cap = cap_m.group(1).strip() if cap_m else ""
            repl[token] = f"![{cap}](../../BookTEX/figures/{img}.png)"
        return "\n\n" + token + "\n\n"

    return FIG_RE.sub(sub, tex), repl


def run_pandoc(tex: str) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".tex", delete=False, encoding="utf-8") as f:
        f.write(tex); tmp = f.name
    try:
        res = subprocess.run(
            ["quarto", "pandoc", tmp, "-f", "latex", "-t", "markdown",
             "--wrap=preserve", "--markdown-headings=atx"],
            capture_output=True, text=True, encoding="utf-8",
        )
        if res.returncode != 0:
            raise RuntimeError(res.stderr)
        return res.stdout
    finally:
        os.unlink(tmp)


def postclean(md: str) -> str:
    md = re.sub(r"^(#+ .*?)\s*\{#[^}]*\}\s*$", r"\1", md, flags=re.M)  # buang {#id} di heading
    md = re.sub(r"\n{3,}", "\n\n", md)                                 # rapatkan baris kosong
    return md.strip() + "\n"


def reverse_chapter(stem: str) -> None:
    tex_path = CH_DIR / f"{stem}.tex"
    if not tex_path.exists():
        print(f"  {stem}: .tex tidak ada, dilewati"); return
    body = get_body(tex_path)
    body, repl = restore_figures(body, stem)
    md = run_pandoc(preclean(body))
    for token, block in repl.items():
        md = re.sub(r"^\s*" + token + r"\s*$", lambda _m, b=block: b, md, flags=re.M)
    md = postclean(md)
    (QMD_DIR / f"{stem}.qmd").write_text(md, encoding="utf-8")
    print(f"  {stem}: {len(repl)} gambar dipulihkan, {len(md.splitlines())} baris qmd")


def main() -> None:
    stems = [a for a in sys.argv[1:] if not a.startswith("-")] or [f"ch{n:02d}" for n in range(1, 18)]
    print(f"Reverse-sync {len(stems)} bab: .tex -> .qmd")
    for s in stems:
        reverse_chapter(s)
    print("Selesai.")


if __name__ == "__main__":
    main()
