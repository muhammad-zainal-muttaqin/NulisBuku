# Rekayasa Fitur Modern

> Representasi Data untuk *Machine Learning* dan *Deep Learning*
> Penulis: Fatma Indriani

Repo ini berisi **sumber** buku *Rekayasa Fitur Modern* beserta *pipeline* penulisannya.
Buku ditulis dalam format [Quarto](https://quarto.org) dan bisa di-render menjadi
**website (HTML)** dan **dokumen Word (DOCX)**.

---

## 📖 Cara melihat hasil (website & DOCX)

Output hasil render (`website/_book/`) **tidak ikut disimpan di repo** karena bisa
dibuat ulang dari sumber. Jadi untuk melihatnya, render dulu secara lokal:

### 1. Pasang Quarto
Unduh & install dari <https://quarto.org/docs/get-started/>.
Cek instalasi:
```bash
quarto --version
```

### 2. Render seluruh buku (HTML + DOCX sekaligus)
Dari folder `website/`:
```bash
cd website
quarto render
```
Hasilnya muncul di `website/_book/`:
- **Website** → buka `website/_book/index.html` di browser
  (tiap bab juga ada: `website/_book/chapters/ch01.html` … `ch17.html`)
- **DOCX** → `website/_book/Rekayasa-Fitur-Modern.docx`

### 3. Preview website dengan live-reload (opsional)
```bash
cd website
quarto preview
```
Quarto otomatis membuka browser dan me-refresh tiap kali file `.qmd` diubah.

### Render satu format saja
```bash
quarto render --to html    # hanya website
quarto render --to docx    # hanya DOCX
```

> **Catatan Windows:** kalau perintah `quarto` belum dikenali di terminal,
> panggil langsung lewat path lengkap:
> `& "C:\Program Files\Quarto\bin\quarto.exe" render`

---

## 🗂️ Struktur proyek

```
NulisBuku/
├── AGENTS.md                 # Aturan & instruksi untuk AI agent (WAJIB dibaca)
├── pipeline/                 # Sumber kebenaran: rencana, outline, gaya tulis, glosarium
│   ├── book-pipeline-plan.md
│   ├── chapter-subsection-breakdown.md
│   ├── outline-rekayasa-fitur.md
│   ├── writer-system-prompt.md
│   ├── glossary-seed.md
│   └── RULE.md
├── briefs/                   # Brief per subbab (ch01_s01.json, …) — input penulisan
├── drafts/                   # Draf mentah per subbab (ch01_s01.md, …)
├── .blind/                   # Draf "blinded" untuk review
├── website/                  # Proyek Quarto (sumber buku)
│   ├── _quarto.yml           # Konfigurasi buku & format output
│   ├── index.qmd             # Halaman pengantar
│   ├── chapters/             # Isi tiap bab (ch01.qmd … ch17.qmd)
│   └── _book/                # ← OUTPUT render (di-gitignore, tidak di-commit)
├── BookTEX/                  # Jalur naskah FINAL: LaTeX → PDF B5 (lihat BookTEX/README.md)
│   ├── main.tex              # Berkas induk (\input semua bab)
│   ├── preamble.tex          # Tata letak B5, paket, gaya kode
│   ├── chapters/             # ch01.tex … ch17.tex (dari .qmd)
│   ├── figures/              # PNG diagram mermaid
│   └── tools/convert.py      # .qmd → .tex
├── integrate_drafts.py       # Gabungkan drafts/ → website/chapters/*.qmd
├── sync.ps1                  # Sinkronkan SEMUA format sekaligus (lihat di bawah)
└── pipeline.py               # Orkestrasi pipeline penulisan
```

---

## 🔁 Alur kerja penulisan → buku

1. **Brief** disusun di `briefs/` (per subbab).
2. **Draf** ditulis di `drafts/` mengikuti `briefs/` dan aturan di `pipeline/`.
3. Jalankan integrasi untuk menyalin draf ke bab Quarto:
   ```bash
   python integrate_drafts.py
   ```
   Skrip ini menggabungkan semua `drafts/chXX_sYY.md` menjadi
   `website/chapters/chXX.qmd` dan menyesuaikan level heading.
4. **Render** buku (lihat bagian *Cara melihat hasil* di atas).

---

## 🔄 Sinkronisasi semua format (satu perintah)

**Sumber utama konten = LaTeX (`BookTEX/chapters/*.tex`).** Naskah final disunting
di sana; website di-*generate* balik agar tetap sinkron sebagai *online resources*.

```
BookTEX/*.tex ──► tectonic          ──► PDF B5 (naskah final)
             └──► reverse.py (.qmd) ──► quarto render ──► website (HTML/DOCX + notebook)
```

Satu perintah menjalankan seluruh rantai:

```powershell
./sync.ps1                 # dari .tex: build PDF + update .qmd + render website
./sync.ps1 -PdfOnly        # cuma build PDF B5
./sync.ps1 -SkipRender     # update .qmd tapi lewati 'quarto render' (cepat)
./sync.ps1 -SkipWeb        # cuma PDF, jangan sentuh website
./sync.ps1 -Status         # laporan status, tidak mengubah apa pun
```

Tahap arah utama:

| # | Dari → Ke | Alat |
|---|-----------|------|
| 1 | `BookTEX/main.tex` → PDF B5               | `tectonic` |
| 2 | `BookTEX/chapters/*.tex` → `website/chapters/*.qmd` | `BookTEX/tools/reverse.py` |
| 3 | `.qmd` → website HTML/DOCX                 | `quarto render` |

**Diagram tetap hidup:** `convert.py` menyimpan sumber mermaid di
`BookTEX/figures/_src/chNN.json`; `reverse.py` memasangnya kembali sebagai blok
```` ```{mermaid} ```` di `.qmd`, jadi website tetap punya diagram interaktif (bukan
sekadar PNG).

> `.qmd` sekarang **berkas turunan** (seperti output build) — jangan disunting
> tangan; suntingan akan tertimpa saat sync berikutnya. Perbaiki konten di `.tex`.

### Arah balik (jarang): impor konten dari website ke `.tex`

Kalau perlu menarik konten `.qmd` → `.tex` (mis. bootstrap awal):

```powershell
./sync.ps1 -FromQmd        # qmd -> tex; lewati bab yang .tex-nya sudah disunting manual
./sync.ps1 -FromQmd -Force # paksa timpa .tex
```

Pengaman: `convert.py` menyimpan `qmd-sha1`/`tex-sha1` di kepala tiap `.tex` dan
**melewati** bab yang sudah disunting manual kecuali `-Force`. Cek dulu dengan
`./sync.ps1 -Status` (`[BENTROK]` = `.qmd` & `.tex` sama-sama berubah).

> Catatan: `drafts/*.md` + `integrate_drafts.py` adalah sisa fase generasi awal
> (draf AI). Sekarang konten hidup di `.tex`; `drafts/` tinggal arsip.

---

## ⚠️ Aturan penting saat menulis / build

Diambil dari `AGENTS.md` — patuhi agar penomoran Quarto tidak rusak:

- **Jangan menulis nomor bab/subbab secara manual** pada heading.
  Quarto menomori otomatis.
  - ❌ `## 14.1 Judul Sub-Bab`
  - ✅ `## Judul Sub-Bab`
- **Hierarki heading tidak boleh melompat.** Gunakan berurutan:
  `#` (bab) → `##` (subbab) → `###` (sub-subbab).
  Jangan langsung pakai `####` sebelum ada `##`/`###`, karena penomoran bisa
  jadi kacau seperti `14.0.0.1`.
- Sebelum mengubah konten, **baca dulu** seluruh file di `pipeline/` —
  itu sumber kebenaran untuk struktur, gaya, dan istilah.

---

## 🔒 Yang tidak ikut di repo

File berikut sengaja di-`.gitignore`:
- `.secret/`, `.antigravitycli/` — kredensial/konfigurasi pribadi
- `website/_book/`, `website/.quarto/`, `website/index.tex`, `_build/` — output build (regenerable)
- file temp & cache tool

Untuk mendapatkan website/DOCX, cukup **render ulang** dari sumber.
