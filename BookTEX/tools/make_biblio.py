#!/usr/bin/env python3
r"""Bangkitkan daftar-pustaka.tex (master Daftar Pustaka) dari references.bib.

Memakai pandoc --citeproc dengan `nocite: '@*'` sehingga SELURUH entri .bib
tampil (author-year), lalu dibungkus sebagai bab tak bernomor 'Daftar Pustaka'.
Di-\input di bagian belakang buku (main.tex).

Pemakaian:  python tools/make_biblio.py
"""
from __future__ import annotations
import subprocess, tempfile, os
from pathlib import Path

OUT_ROOT = Path(__file__).resolve().parents[1]
BIB = OUT_ROOT / "references.bib"
OUT = OUT_ROOT / "daftar-pustaka.tex"

STUB = "---\nnocite: '@*'\n---\n\n::: {#refs}\n:::\n"

def main() -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(STUB); tmp = f.name
    try:
        res = subprocess.run(
            ["pandoc", tmp, "-f", "markdown", "-t", "latex",
             "--citeproc", f"--bibliography={BIB}", "--wrap=preserve"],
            capture_output=True, text=True, encoding="utf-8",
        )
        if res.returncode != 0:
            raise RuntimeError(res.stderr)
        body = res.stdout
    finally:
        os.unlink(tmp)

    header = (
        "% ==========================================================================\n"
        "% daftar-pustaka.tex — master bibliografi, dibangkitkan oleh tools/make_biblio.py\n"
        "% Jangan sunting manual; sunting references.bib lalu jalankan ulang.\n"
        "% ==========================================================================\n"
        "\\chapter*{Daftar Pustaka}\n"
        "\\addcontentsline{toc}{chapter}{Daftar Pustaka}\n"
        "\\markboth{Daftar Pustaka}{}\n\n"
    )
    OUT.write_text(header + body, encoding="utf-8")
    n = body.count("\\bibitem")
    print(f"daftar-pustaka.tex: {n} entri")

if __name__ == "__main__":
    main()
