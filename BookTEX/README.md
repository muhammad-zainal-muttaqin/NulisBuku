# BookTEX — Rekayasa Fitur Modern (naskah LaTeX, B5)

Jalur naskah **final** buku *Rekayasa Fitur Modern* dalam bentuk LaTeX,
menghasilkan **PDF ukuran B5** (176 × 250 mm) yang sudah dilayout.

Dibuat atas arahan (7 Juli 2026):
naskah final = PDF terlayout B5, sumber LaTeX, subbab maksimal 1 level,
satu berkas per bab.

## Struktur

```
BookTEX/
├── main.tex           # berkas induk: \input semua bab
├── preamble.tex       # kelas, tata letak B5, paket, gaya kode
├── metadata.tex       # judul, penulis, halaman judul
├── chapters/          # ch01.tex … ch17.tex (SUMBER naskah, satu berkas per bab)
├── figures/           # PNG diagram
│   └── _src/          # sumber mermaid per bab (chNN.json) untuk reverse-sync
├── tools/
│   ├── convert.py     # .qmd → .tex (arah balik / bootstrap)
│   └── reverse.py     # .tex → .qmd (arah utama, untuk website)
├── build.ps1          # skrip kompilasi PDF saja
└── .gitignore
```

## Kompilasi

Butuh **Tectonic** (mesin LaTeX mandiri; paket diunduh saat pertama dipakai —
tak perlu instalasi TeX Live besar).

```powershell
./build.ps1                # kompilasi -> main.pdf
./build.ps1 -Convert       # regen .tex dari .qmd dulu, lalu kompilasi
```

atau langsung:

```powershell
tectonic main.tex
```

## Menyunting

`chapters/chNN.tex` adalah **sumber utama naskah** — sunting langsung di sini.
Setelah menyunting, jalankan `../sync.ps1` (dari root repo) untuk:

1. build PDF B5 (`tectonic`),
2. update `website/chapters/*.qmd` (`tools/reverse.py`),
3. render website (`quarto render`).

Diagram mermaid tetap hidup di website: sumbernya disimpan di
`figures/_src/chNN.json` saat konversi awal, lalu dipasang kembali oleh
`reverse.py`. Kalau kamu menambah gambar baru langsung di `.tex`
(`\includegraphics`), website memakainya sebagai PNG biasa.

- `tools/convert.py` = arah balik (`.qmd → .tex`), dipakai untuk bootstrap awal
  atau menarik perubahan dari website. Ada pengaman hash: bab yang `.tex`-nya
  sudah disunting manual **dilewati** (kecuali `--force`). Cek: `../sync.ps1 -Status`.
- `tools/reverse.py` = arah utama (`.tex → .qmd`).

## Keputusan tata letak

| Aturan            | Implementasi |
|----------------------------|--------------|
| PDF terlayout, ukuran B5   | `geometry` `b5paper`, kelas `book` `twoside` |
| Sumber LaTeX               | pandoc `.qmd` → `.tex`, kompilasi Tectonic |
| Subbab maksimal 1 level    | `secnumdepth=1`, `tocdepth=1` → hanya Bab + Subbab bernomor; `###` lama jadi kepala tak bernomor |
| Satu berkas per bab        | `chapters/chNN.tex`, dirangkai `\input` di `main.tex` |
| Rumus & kode enak dibaca   | `amsmath`; `listings` gaya Python |

## Catatan / perlu dicek

- **Gambar ch01, ch02, ch05**: jumlah PNG hasil render lama lebih banyak dari
  jumlah diagram di `.qmd` (kemungkinan sisa render lama). Pemetaan memakai urutan
  kemunculan (fig-1, fig-2, …); **cek visual** apakah gambar cocok dengan caption.
- Peringatan *overfull/underfull hbox* saat kompilasi bersifat kosmetik
  (baris/kotak sedikit meluber) — dirapikan saat penyeliaan tata letak.
