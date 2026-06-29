# Project: Rekayasa Fitur Modern - Agent System Instructions

This file is the **master instruction manual** for any AI Agent working on this repository.

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
