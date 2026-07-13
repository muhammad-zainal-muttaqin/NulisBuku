#!/usr/bin/env python3
r"""Hitung lebar cetak tiap figures/*.pdf (mermaid) -> figures/sizes.json.

Masalah: LaTeX dulu memaksa semua gambar mermaid ke width=0.92\linewidth
tanpa peduli rasio aslinya. Karena huruf label mermaid berukuran piksel
tetap, diagram yang secara alami sempit (sedikit node) jadi meluber jadi
±20pt saat dipaksa selebar itu, sementara diagram yang lebar (banyak node)
malah mengecil sampai ±5pt. Skrip ini mengukur font asli tiap PDF (dari span
teks, bukan tebakan), lalu memilih skala sehingga:

  1) ukuran huruf tercetak sedekat mungkin ke target (9.5pt), TAPI
  2) tidak pernah melebihi lebar teks B5 maupun tinggi maksimum per gambar.

Hasil (lebar & tinggi mm per figur) ditulis ke figures/sizes.json; dibaca
oleh md2tex.py saat menyisipkan \includegraphics. Diagram yang tetap
< 8pt walau sudah dibatasi kotak halaman berarti butuh perombakan struktur
(arah TB/LR, split panel, atau vektor buatan tangan) -- bukan sekadar
skala; skrip ini menandai nama-nama itu di keluaran.

Pemakaian: python tools/size_figs.py   (jalankan ulang tiap kali .mmd
render ulang / dimensi tata letak B5 berubah)
"""
import json, re
from pathlib import Path
import fitz

FIG = Path(__file__).resolve().parents[1] / "figures"

# textwidth/textheight aktual (diukur dari preamble.tex terpasang, lihat
# catatan di tools/README atau jalankan ulang probe _dims.tex bila geometry berubah).
TEXTWIDTH_PT = 341.43309
TEXTHEIGHT_PT = 529.22127
WTARGET = 0.92 * TEXTWIDTH_PT
HCAP = 0.60 * TEXTHEIGHT_PT      # batas tinggi 1 figur agar caption+teks lain muat
TARGET_FONT = 9.5
PT_MM = 0.352778


def is_mermaid_pdf(d: "fitz.Document") -> bool:
    # mmdc merender lewat headless Chromium -> "Skia/PDF" jadi produsen PDF.
    # Ilustrasi pesanan (matplotlib, vektor tangan, dsb.) punya produsen lain
    # dan tidak boleh diskalakan pakai heuristik ukuran-huruf mermaid ini.
    return "skia" in (d.metadata.get("producer") or "").lower()


def natural_size_and_font(pdf_path: Path):
    d = fitz.open(pdf_path)
    if not is_mermaid_pdf(d):
        d.close()
        return None
    pg = d[0]
    w, h = pg.rect.width, pg.rect.height
    sizes = [
        span["size"]
        for block in pg.get_text("dict")["blocks"]
        for line in block.get("lines", [])
        for span in line.get("spans", [])
        if span["text"].strip()
    ]
    d.close()
    return w, h, (max(sizes) if sizes else 0.0)


def main() -> None:
    manifest, need_rework = {}, []
    for p in sorted(FIG.glob("ch*-fig-*.pdf")):
        measured = natural_size_and_font(p)
        if measured is None:
            continue  # bukan mermaid (mis. ilustrasi vektor pesanan) -- lewati
        w, h, maxfont = measured
        scale = min(TARGET_FONT / maxfont if maxfont else 1e9, WTARGET / w, HCAP / h)
        font_final = maxfont * scale
        manifest[p.stem] = {
            "width_mm": round(w * scale * PT_MM, 1),
            "height_mm": round(h * scale * PT_MM, 1),
            "font_pt": round(font_final, 1),
        }
        if font_final < 8.0:
            need_rework.append(p.stem)

    out = FIG / "sizes.json"
    out.write_text(json.dumps(manifest, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"Ditulis {out} ({len(manifest)} figur).")
    if need_rework:
        print(f"Masih < 8pt walau dibatasi kotak halaman ({len(need_rework)}) -- butuh "
              f"perombakan struktur (arah/split/vektor): {', '.join(need_rework)}")


if __name__ == "__main__":
    main()
