#!/usr/bin/env python3
r"""v2/drafts/Prakata.txt -> prakata.tex (bagian depan, tak bernomor).

Sumber kebenaran = draf markdown; jangan sunting prakata.tex manual, jalankan
ulang skrip ini. Sama pola dengan tools/make_biblio.py.

Pemakaian: python tools/make_prakata.py
"""
import re, subprocess
from pathlib import Path

OUT_ROOT = Path(__file__).resolve().parents[1]                       # .../BookTEX
SRC = OUT_ROOT.parents[1] / "v2" / "drafts" / "Prakata.txt"
OUT = OUT_ROOT / "prakata.tex"


def main() -> None:
    md = SRC.read_text(encoding="utf-8")
    # Buang judul "# Prakata" markdown -- kepala bagian dibuat manual di bawah,
    # sisanya (paragraf prosa + *emphasis*) dikonversi lewat pandoc.
    md = re.sub(r"^#\s+Prakata\s*\n+", "", md, count=1)

    res = subprocess.run(
        ["pandoc", "-f", "markdown", "-t", "latex", "--wrap=preserve"],
        input=md, capture_output=True, text=True, encoding="utf-8",
    )
    if res.returncode != 0:
        raise RuntimeError(res.stderr)
    body = res.stdout.replace("\r\n", "\n")

    # Blok tanda tangan penutup ("Kota, Bulan Tahun" / "Penulis") -- dua baris
    # tanpa baris kosong di antaranya jadi satu baris mengalir di LaTeX kalau
    # dibiarkan; render rata kanan dengan pemutus baris eksplisit.
    body = re.sub(
        r"\n([^\n]+)\nPenulis\s*$",
        r"\n\\begin{flushright}\n\1\\\\\nPenulis\n\\end{flushright}\n",
        body.rstrip() + "\n",
    )

    tex = (
        "% ==========================================================================\n"
        "% prakata.tex -- dihasilkan dari v2/drafts/Prakata.txt oleh tools/make_prakata.py\n"
        "% Jangan sunting manual; sunting draf lalu jalankan ulang skrip ini.\n"
        "% ==========================================================================\n"
        "% Bab bernomor punya kotak angka besar (58pt) di atas judul yang secara\n"
        "% alami mendorong judul turun; \\chapter* tak punya angka jadi judulnya\n"
        "% nempel ke atas halaman. \\vspace* biasa sebelum \\chapter* tak berpengaruh\n"
        "% (chapter* memicu clearpage sendiri lalu membuang ruang tertunda), jadi\n"
        "% ruang ditambahkan lewat override titleformat lokal (di dalam grup, tak\n"
        "% memengaruhi bab tak bernomor lain seperti Panduan/Daftar Pustaka).\n"
        "\\begingroup\n"
        "\\titleformat{\\chapter}[display]{\\sffamily}{}{0pt}"
        "{\\vspace*{65pt}\\Huge\\bfseries\\color{black}\\raggedright}"
        "[\\vspace{7pt}{\\color{rulegray}\\titlerule[1.4pt]}]\n"
        "\\chapter*{Prakata}\n"
        "\\addcontentsline{toc}{chapter}{Prakata}\n"
        "\\markboth{Prakata}{}\n\n"
        f"{body}\n"
        "\\endgroup\n"
    )
    OUT.write_text(tex, encoding="utf-8")
    print(f"wrote {OUT} ({len(tex.splitlines())} baris)")


if __name__ == "__main__":
    main()
