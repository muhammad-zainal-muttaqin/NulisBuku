#!/usr/bin/env python3
"""Rasterisasi halaman PDF -> PNG (tanpa poppler; pakai PyMuPDF).

Pemakaian:
  python tools/pdf2png.py main.pdf out_dir [dpi]
  python tools/pdf2png.py main.pdf out_dir 150 3-6   # hanya halaman 3..6
"""
import sys
from pathlib import Path
import fitz

def main() -> None:
    pdf = Path(sys.argv[1])
    out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 150
    rng = sys.argv[4] if len(sys.argv) > 4 else None
    doc = fitz.open(pdf)
    pages = range(len(doc))
    if rng:
        a, _, b = rng.partition("-")
        pages = range(int(a) - 1, (int(b) if b else int(a)))
    zoom = dpi / 72
    for i in pages:
        pix = doc[i].get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        f = out / f"{pdf.stem}-p{i+1:02d}.png"
        pix.save(f)
        print(f"  {f}  ({pix.width}x{pix.height})")

if __name__ == "__main__":
    main()
