# BookTEX — Rekayasa Fitur Modern (naskah LaTeX)

Jalur naskah **final** buku *Rekayasa Fitur Modern* dalam bentuk LaTeX,
menghasilkan PDF ukuran 155×230mm yang sudah dilayout.

## Struktur

```
BookTEX/
├── main.tex              # berkas induk: \input semua bab + lampiran
├── preamble.tex          # kelas, tata letak, paket, gaya kode/tabel
├── metadata.tex          # judul, penulis, halaman judul
├── prakata.tex           # Prakata (dihasilkan tools/make_prakata.py)
├── panduan.tex           # Cara Menggunakan Buku Ini (tools/make_panduan.py)
├── daftar-pustaka.tex    # Daftar pustaka (tools/make_biblio.py)
├── tentang-penulis.tex   # Tentang Penulis (tools/make_tentang_penulis.py)
├── chapters/             # ch01.tex … ch17.tex + lampiran-{A,B,C}.tex
├── figures/               # PNG/JPG ilustrasi + PDF vektor (mermaid/matplotlib)
│   ├── sizes.json         # manifest lebar-cetak lama dari tools/size_figs.py
│   ├── image-version-comparison.md
│   ├── _originals_precrop/  # backup lokal, tak masuk git (lihat .gitignore)
│   └── _replaced_mermaid/   # arsip diagram mermaid lama, tak masuk git
├── cover-front.png, cover-back.png   # sampul (dipakai main-review.pdf)
├── tools/                 # skrip generator .tex dari sumber v2/drafts
├── build.ps1              # kompilasi main.pdf
└── .gitignore
```

Sumber naskah per bab ada di `v2/drafts/chNN/chNN_draft_v2.md` (satu level
di atas `NulisBuku/`). `tools/md2tex.py` mengonversinya menjadi
`chapters/chNN.tex`. File `.tex` boleh disunting manual — menjalankan ulang
`md2tex.py` pada bab yang sudah disunting akan **dilewati** kecuali dipaksa,
jadi suntingan manual di `chapters/*.tex` aman.

## Kompilasi

Butuh **Tectonic** (mesin LaTeX mandiri; paket diunduh saat pertama dipakai)
dan `mmdc` (Mermaid CLI, untuk merender ulang diagram jika sumber `.mmd`
berubah).

```powershell
./build.ps1
# atau langsung:
tectonic -X compile main.tex
```

### main-review.pdf (versi ringan untuk editor/kolega)

`main.pdf` memakai gambar resolusi penuh (cocok cetak, tapi besar — puluhan
MB). `main-review.pdf` adalah versi sekunder dengan semua gambar
di-downsample ke 300dpi pada ukuran cetak aktualnya lalu dikonversi JPEG
kualitas 88 (kecuali `qr-fe-m.png`, tetap PNG lossless karena pola biner
tajamnya rusak oleh kompresi JPEG), plus sampul depan/belakang disisipkan
sebagai halaman pembuka/penutup. Tidak ada skrip tunggal untuk ini — alurnya:

1. Salin seluruh sumber (`*.tex`, `chapters/`, `tools/`, `figures/*.png|*.pdf`)
   ke folder scratch.
2. Di folder scratch, untuk tiap `figures/*.png`: baca lebar-cetak dari
   `\includegraphics[width=...]{}` di `chapters/*.tex`, resize ke 300dpi pada
   lebar itu, simpan sebagai `.jpg` kualitas 88, hapus `.png` lama.
3. `tectonic -X compile main.tex` di folder scratch → PDF dasar.
4. Sisipkan `cover-front.png`/`cover-back.png` (dikonversi JPEG kualitas 90)
   sebagai halaman pertama/terakhir lewat PyMuPDF, simpan dengan
   `garbage=4, deflate=True, clean=True` (kompresi ulang, penting — tanpa ini
   PyMuPDF menyisipkan gambar tanpa kompresi dan ukurannya membengkak).

## Gambar

- **Ilustrasi** (`figures/chNN-fig-M.png`, sebagian besar bab): dibuat di
  luar repo ini, dipasang langsung. `\includegraphics[width=111.6mm]{...}`
  (90% lebar teks) dipakai seragam supaya semua gambar cukup besar untuk
  dibaca saat dicetak.
- **Diagram vektor** (`figures/chNN-fig-M.pdf`): mermaid via `mmdc`, atau
  matplotlib. Render ulang diagram mermaid dari `.mmd` (di
  `v2/drafts/figures/`) dengan:

  ```powershell
  mmdc -i "../../v2/drafts/figures/chNN-fig-M.mmd" `
       -o "figures/chNN-fig-M.pdf" `
       -c "tools/mermaid-book.json" -f
  ```

  Flag `-f` (`--pdfFit`) **wajib** — tanpa itu mmdc menghasilkan PDF
  berukuran kertas penuh (mis. Letter) dengan diagram kecil di dalamnya
  alih-alih PDF yang pas dengan bounding box diagram.
- `tools/size_figs.py` — heuristik lama yang menghitung lebar-cetak per
  diagram mermaid dari ukuran font aslinya (target ~9.5pt tercetak). Manifest
  hasilnya (`figures/sizes.json`) sudah tak dipakai sejak semua gambar
  diseragamkan ke `width=111.6mm`; skrip ini tinggal untuk referensi bila
  perlu menimbang ulang satu diagram yang aspect ratio-nya sangat curam.

## Keputusan tata letak

| Aturan                      | Implementasi |
|------------------------------|--------------|
| PDF terlayout, ukuran 155×230mm | `geometry` (`paperwidth=155mm,paperheight=230mm`), kelas `book` `twoside` |
| Sumber LaTeX per bab          | `v2/drafts/chNN/*.md` → pandoc/`md2tex.py` → `chapters/chNN.tex` |
| Lampiran (A/B/C)              | `\appendix` + `\titleformat{\chapter}` lokal (kicker "LAMPIRAN X") |
| Gambar selebar mungkin        | `width=111.6mm` (0.90×lebar teks) seragam di semua figure |
| Rumus & kode enak dibaca      | `amsmath`; `listings` gaya Python |

## Catatan

- Peringatan *overfull/underfull hbox* saat kompilasi sebagian besar bersifat
  kosmetik (baris/kotak meluber beberapa poin) — sudah diperiksa, bukan
  regresi baru.
- `suggested-codes-to-add.md` — usulan RA untuk menambah listing kode Python
  ke beberapa bab; belum diterapkan, masih rencana terbuka.
