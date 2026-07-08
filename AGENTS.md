# Project: Rekayasa Fitur Modern - Agent System Instructions

This file is the **master instruction manual** for any AI Agent working on this repository.

## Format & Working Directory Aktif (per 7 Juli 2026)

**Naskah final = PDF terlayout B5 dari LaTeX. Sumber utama konten sekarang di `BookTEX/chapters/chNN.tex`, BUKAN lagi `.qmd`.**

Keputusan Bu Fatma (7 Juli 2026): naskah final berupa **PDF B5** (176×250 mm) yang di-*layout* dari **LaTeX**, satu berkas per bab, subbab maksimal 1 level. Karena itu:

- **Working directory default = `BookTEX/`.** Sunting konten langsung di `BookTEX/chapters/chNN.tex`.
- **`website/chapters/*.qmd` kini berkas TURUNAN** (di-*generate* dari `.tex` lewat `BookTEX/tools/reverse.py`). **Jangan disunting tangan** — suntingan akan tertimpa saat sync berikutnya. Website tetap ada sebagai *online resources* (notebook dll.), tapi ikut dari `.tex`.
- **Sync satu perintah:** `./sync.ps1` (dari root) → build PDF (`tectonic`) + regen `.qmd` + `quarto render`. Cek arah perubahan tanpa mengubah apa pun: `./sync.ps1 -Status`. Detail lengkap: `BookTEX/README.md` dan bagian "Sinkronisasi" di `README.md`.
- **Aturan heading markdown di bawah berlaku untuk `.qmd` (turunan)**; di `.tex`, batas 1 level subbab dijaga oleh `secnumdepth=1`/`tocdepth=1` di `preamble.tex`.

> **Larangan skrip vs. jalur `.tex`:** larangan menulis skrip pemroses massal (di bawah) berlaku untuk **penyuntingan naskah** — perbaikan prosa/kalimat tetap wajib manual-interaktif. `convert.py`/`reverse.py`/`sync.ps1` adalah *tooling konversi format* (bukan penyunting konten) dan dikecualikan.

> **Catatan konflik yang belum diputuskan:** `3-July-2026/chapter-revision-instructions-1.md` (revisi editorial babak-1) meminta **membuang referensi notebook/latihan/mini-project** dari bab (aturan #8), sementara ada jalur kerja terpisah membuat notebook praktik per bab. Ini belum direkonsiliasi — **tanyakan** sebelum menghapus referensi notebook massal.

## The Absolute Mandate
You MUST read and strictly obey the instructions contained in the `pipeline/` directory before taking any action. These files are the single source of truth for the book's content, structure, style, and vocabulary.

**MANDATORY READING LIST:**
Before writing or modifying any content, you MUST execute `read` commands for the following files:
1. `pipeline/book-pipeline-plan.md` - For architecture and workflow.
2. `pipeline/chapter-subsection-breakdown.md` - For the specific scope of the subsection you are working on.
3. `pipeline/outline-rekayasa-fitur.md` - For global book structure and constraints.
4. `pipeline/writer-system-prompt.md` - For the exact voice, tone, style, and paragraph guidelines.
5. `pipeline/glossary-seed.md` - For the mandatory terminology policy.
6. `pipeline/RULE.md` - For project boundaries.

Do NOT rely on summary instructions. Read the actual pipeline files. The instructions there are hard rules, not suggestions.
### Aturan Penomoran Heading (Format Markdown)
- **Dilarang Menulis Nomor Bab/Sub-bab Secara Manual:** Pada saat menulis draf, jangan menaruh angka hierarki pada judul *heading* (Contoh SALAH: ## 14.1 Judul Sub-Bab). Quarto akan memberikan penomoran secara otomatis. Tulislah hanya teks judulnya saja (Contoh BENAR: ## Judul Sub-Bab).
- **Hierarki *Heading* Tidak Boleh Melompat:** Gunakan level # untuk judul Bab utama, ## untuk sub-bab level 1, ### untuk sub-bab level 2, dst. Jangan menggunakan #### secara langsung jika belum ada ## dan ### di atasnya, karena mesin *renderer* (Quarto) akan bingung dan menghasilkan penomoran seperti 14.0.0.1.
- **Dilarang Keras Merancang/Menulis Skrip Otomatisasi (Python, Bash, dll.) untuk Memodifikasi Naskah:** AI Agent wajib bekerja menggunakan kapabilitas kognitif aslinya secara interaktif dan langsung memodifikasi *file* menggunakan *tools* yang tersedia (seperti `edit` atau `write`). Menggunakan skrip pemrosesan massal (seperti skrip regex) merusak alur natural bahasa (*flow*) dan menyisipkan kekakuan tata bahasa yang terdengar seperti robot (*AI slop*). Pekerjaan penyuntingan harus dieksekusi secara manual-interaktif di bawah pengawasan langsung (*supervised live*).

### Aturan Audit Bahasa dan Penghapusan AI Slop (Style Guide)
Pengalaman audit pada Bab 1 hingga Bab 5 menetapkan standar emas (*gold standard*) berikut untuk proses penyuntingan dan penulisan naskah:
- **Narasi Paragraf di Atas Daftar (*List Fatigue*):** Hindari penggunaan *bullet list* (`-` atau `*`) secara berlebihan. Jika poin-poin penjelasan dapat dibaca berkesinambungan, lebur poin-poin tersebut menjadi paragraf naratif yang luwes dengan kata sambung natural (misal: "Pertama, ... Kedua, ... Terakhir, ...").
- **Aturan Ketat Penomoran (*Numbered List*):** Angka `1., 2., 3.` HANYA boleh digunakan mutlak untuk urutan proses, kronologi, langkah-langkah prosedural, atau peringkat. Dilarang keras menggunakan angka untuk menyebutkan opsi, klasifikasi, variasi, atau karakteristik yang kedudukannya setara.
- **Integrasi Keterangan Rumus Matematis:** Dilarang menjelaskan variabel dari sebuah persamaan matematika menggunakan *bullet list* yang kaku (Contoh SALAH: "Di mana: \n - x = ... \n - y = ..."). Keterangan variabel wajib dilebur ke dalam kalimat naratif penyerta (Contoh BENAR: "Dalam perumusan tersebut, $x$ melambangkan ... sedangkan $y$ mewakili ...").
- **Penghapusan Transisi Robotik (*AI Slop*):** Hapus kalimat pengantar usang dan kaku khas AI seperti "Berikut adalah beberapa karakteristik utama:", "Terdapat tiga kelemahan yaitu:", atau "Di bawah ini adalah penjelasannya:". Langsung hubungkan paragraf dengan transisi makna yang mulus dan masuk ke inti pembahasan.
- **Efisiensi Kata & Konteks (*Direct & Intuitive*):** Buang kata-kata *filler* yang membuat kalimat membengkak. Fokus pada penyampaian intuisi dari sebuah konsep *machine learning* layaknya seorang dosen yang sedang menjelaskan langsung kepada mahasiswanya secara terstruktur, membumi, dan tidak menggurui.
- **Redam Drama & Verba Reaktif (Gaya Akademik Indonesia):** Bahasa Indonesia akademik sangat elegan jika ditulis secara deskriptif/pasif, tanpa perlu menggunakan kata kerja/sifat yang berlebihan (*verb-heavy*). Hapus kata-kata seperti "mematikan", "liar", "brutal", "menabrak", "menginfeksi". Gunakan susunan yang lebih tenang dan *to the point*.
  - *Contoh SALAH:* "Seorang penguji melakukan uji coba secara liar, menyebabkan anomali pada penelitian."
  - *Contoh BENAR:* "Seorang peneliti melakukan uji coba dengan sembarangan, sehingga menyebabkan anomali pada hasil penelitian."
- **Pertahankan Terminologi Industri (Hindari *Over-localization*):** Jangan memaksa menerjemahkan istilah *lingua franca* atau sengaja diserap luas hanya demi menghindari bahasa Inggris. Memaksa mengubah *leakage* menjadi "kebocoran", atau *pipeline* menjadi "saluran" secara berulang akan sangat canggung. Sesuai Living Glossary, pertahankan istilah industri tersebut dalam bentuk aslinya dan cetak miring (*italic*).

### Aturan Desain Visual & Pembuatan Diagram (Mermaid Style Guide)
- **Prinsip Cetak Hitam-Putih (Monokrom):** Buku ini didesain untuk dicetak secara fisik dalam format grayscale/hitam-putih. Seluruh diagram wajib menggunakan skema warna monokromatik/netral. Dilarang keras menggunakan warna-warni kustom (pastel, merah, hijau, biru, oranye) yang akan tampak berlumpur atau tidak kontras saat dicetak hitam-putih.
- **Wajib Solid White untuk Latar Belakang Label Panah (Pencegahan Bug Rendering):** Jangan menggunakan latar belakang transparan atau 'none' untuk teks penjelasan panah (edge label). Headless browser/Puppeteer pada sistem operasi Windows akan merender transparansi tersebut menjadi kotak abu-abu gelap atau hitam pekat di dalam dokumen Word (DOCX). Atur `edgeLabelBackground` secara eksplisit menjadi solid white (`#ffffff`).
- **Gunakan Inisialisasi Tema Netral Global:** Setiap kode Mermaid wajib menggunakan inisialisasi tema `neutral` dan menyetel `edgeLabelBackground` ke `#ffffff`. Contoh deklarasi standar yang wajib diikuti di awal diagram:
  ```mermaid
  %%{init: {'theme': 'neutral', 'themeVariables': { 'edgeLabelBackground': '#ffffff' }}}%%
  graph TD
      ...
  ```
- **Hapus Semua Style Manual Berwarna:** Dilarang menggunakan baris `style Node fill:#XXXXXX,stroke:#YYYYYY` yang menyisipkan warna kustom. Biarkan tema `neutral` global yang mengatur warna kotak dan garis agar seragam dan bersih di seluruh buku.
