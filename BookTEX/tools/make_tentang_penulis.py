#!/usr/bin/env python3
r"""v2/drafts/Tentang penulis.txt -> tentang-penulis.tex (bagian belakang, tak bernomor).

Sumber kebenaran = draf teks; jangan sunting tentang-penulis.tex manual, jalankan
ulang skrip ini. Sama pola dengan tools/make_prakata.py. Tiap paragraf draf =
satu penulis, kalimat pertama "<Nama> adalah ..." -> nama dipisah jadi kepala
run-in (\penulisnama), sisanya jadi paragraf biografi.

Pemakaian: python tools/make_tentang_penulis.py
"""
import re, subprocess
from pathlib import Path

OUT_ROOT = Path(__file__).resolve().parents[1]                       # .../BookTEX
SRC = OUT_ROOT.parents[1] / "v2" / "drafts" / "Tentang penulis.txt"
OUT = OUT_ROOT / "tentang-penulis.tex"


def to_latex(text: str) -> str:
    res = subprocess.run(
        ["pandoc", "-f", "markdown", "-t", "latex", "--wrap=preserve"],
        input=text, capture_output=True, text=True, encoding="utf-8",
    )
    if res.returncode != 0:
        raise RuntimeError(res.stderr)
    return res.stdout.strip()


def main() -> None:
    raw = SRC.read_text(encoding="utf-8")
    raw = re.sub(r"^Tentang Penulis\s*\n+", "", raw, count=1)
    paras = [p.strip() for p in re.split(r"\n\s*\n", raw) if p.strip()]

    blocks = []
    for para in paras:
        m = re.match(r"^(.+?)\s+(adalah\s.*)$", para, re.S)
        if not m:
            raise RuntimeError(f"tak bisa mengambil nama dari paragraf: {para[:60]!r}")
        name, rest = m.group(1), m.group(2)
        name_tex = to_latex(name)
        # Nama diulang: sekali sebagai kepala run-in (\penulisnama), sekali lagi
        # di awal paragraf biografi ("<Nama> adalah ...") sesuai gaya yang diminta.
        body_tex = to_latex(f"{name} {rest}")
        blocks.append(
            f"\\penulisnama{{{name_tex}}}\n"
            f"\\noindent {body_tex}\\par\n"
        )

    body = "\n\\penulisjeda\n\n".join(blocks)

    tex = (
        "% ==========================================================================\n"
        "% tentang-penulis.tex -- dihasilkan dari v2/drafts/Tentang penulis.txt oleh\n"
        "% tools/make_tentang_penulis.py. Jangan sunting manual; sunting draf lalu\n"
        "% jalankan ulang skrip ini.\n"
        "% ==========================================================================\n"
        "\\chapter*{Tentang Penulis}\n"
        "\\addcontentsline{toc}{chapter}{Tentang Penulis}\n"
        "\\markboth{Tentang Penulis}{}\n\n"
        f"{body}\n"
    )
    OUT.write_text(tex, encoding="utf-8")
    print(f"wrote {OUT} ({len(tex.splitlines())} baris)")


if __name__ == "__main__":
    main()
