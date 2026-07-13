#!/usr/bin/env python3
r"""Buat figures/qr-fe-m.png -- QR code ke situs pendamping buku.

Dipakai oleh panduan.tex (kotak `sumberdaring`, lihat tools/make_panduan.py).
Jalankan ulang hanya jika URL situs berubah.

Pemakaian: python tools/make_qr.py
"""
from pathlib import Path
import qrcode

URL = "https://fe-m.pages.dev/"
OUT = Path(__file__).resolve().parents[1] / "figures" / "qr-fe-m.png"


def main() -> None:
    img = qrcode.make(URL, box_size=20, border=2,
                       error_correction=qrcode.constants.ERROR_CORRECT_M)
    img.save(OUT)
    print(f"wrote {OUT} ({img.size[0]}x{img.size[1]}) -> {URL}")


if __name__ == "__main__":
    main()
