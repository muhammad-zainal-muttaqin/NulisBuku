#!/usr/bin/env python3
r"""v2/drafts/Cara menggunakan buku.txt -> panduan.tex (bagian depan, tak bernomor).

Sumber kebenaran = draf teks; jangan sunting panduan.tex manual, jalankan
ulang skrip ini. Sama pola dengan tools/make_prakata.py, ditambah satu blok
khusus: [SUMBERDARING]...[/SUMBERDARING] di draf menandai paragraf yang harus
masuk kotak `sumberdaring` (preamble.tex) berdampingan dengan QR code
(figures/qr-fe-m.png, dibuat oleh tools/make_qr.py) memakai minipage dua
kolom. Blok itu diubah ke pandoc raw-LaTeX fence (```{=latex}) sebelum
berkas penuh dijalankan lewat satu pemanggilan pandoc, sama seperti
md2tex.py menangani GAMBAR/tabeljudul/dsb.

Pemakaian: python tools/make_panduan.py
"""
import re, subprocess, tempfile, os
from pathlib import Path

OUT_ROOT = Path(__file__).resolve().parents[1]                       # .../BookTEX
SRC = OUT_ROOT.parents[1] / "v2" / "drafts" / "Cara menggunakan buku.txt"
OUT = OUT_ROOT / "panduan.tex"

URL_RE = re.compile(r"https?://\S+")
SUMBERDARING_RE = re.compile(
    r"\[SUMBERDARING\]\s*\n(.*?)\n\s*\[/SUMBERDARING\]", re.S
)


def run_pandoc(md: str) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(md); tmp = f.name
    try:
        res = subprocess.run(
            ["pandoc", tmp, "-f", "markdown+raw_attribute", "-t", "latex",
             "--wrap=preserve"],
            capture_output=True, text=True, encoding="utf-8",
        )
        if res.returncode != 0:
            raise RuntimeError(res.stderr)
        return res.stdout
    finally:
        os.unlink(tmp)


def sumberdaring_block(paragraph: str) -> str:
    m = URL_RE.search(paragraph)
    if not m:
        raise RuntimeError("blok [SUMBERDARING] tidak memuat URL")
    raw = m.group(0)
    url = raw.rstrip(",.;:)")  # buang tanda baca kalimat yang ikut tertangkap...
    trailing_punct = raw[len(url):]  # ...tapi jangan hilang dari kalimatnya
    placeholder = "@@URL@@"
    text_with_placeholder = (
        paragraph[:m.start()] + placeholder + trailing_punct + paragraph[m.end():]
    )
    prose = run_pandoc(text_with_placeholder).strip()
    href = f"\\href{{{url}}}{{\\texttt{{{url}}}}}"
    prose = prose.replace(placeholder, href)
    return (
        "```{=latex}\n"
        "\\begin{sumberdaring}\n"
        "\\noindent\\begin{minipage}[t]{24mm}\\vspace{0pt}\n"
        "\\includegraphics[width=22mm]{qr-fe-m}\n"
        "\\end{minipage}\\hfill\n"
        "\\begin{minipage}[t]{\\linewidth-28mm}\\vspace{0pt}\n"
        f"\\noindent {prose}\n"
        "\\end{minipage}\n"
        "\\end{sumberdaring}\n"
        "```"
    )


def main() -> None:
    md = SRC.read_text(encoding="utf-8")
    md = re.sub(r"^#\s+Cara Menggunakan Buku Ini\s*\n+", "", md, count=1)

    m = SUMBERDARING_RE.search(md)
    if not m:
        raise RuntimeError("blok [SUMBERDARING]...[/SUMBERDARING] tidak ditemukan di draf")
    md = md[:m.start()] + sumberdaring_block(m.group(1).strip()) + md[m.end():]

    body = run_pandoc(md)

    tex = (
        "% ==========================================================================\n"
        "% panduan.tex -- dihasilkan dari v2/drafts/Cara menggunakan buku.txt oleh\n"
        "% tools/make_panduan.py. Jangan sunting manual; sunting draf lalu jalankan\n"
        "% ulang skrip ini.\n"
        "% ==========================================================================\n"
        "\\chapter*{Cara Menggunakan Buku Ini}\n"
        "\\addcontentsline{toc}{chapter}{Cara Menggunakan Buku Ini}\n"
        "\\markboth{Cara Menggunakan Buku Ini}{}\n\n"
        f"{body}\n"
    )
    OUT.write_text(tex, encoding="utf-8")
    print(f"wrote {OUT} ({len(tex.splitlines())} baris)")


if __name__ == "__main__":
    main()
