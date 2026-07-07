# Audit Gambar dan Placeholder - Rekayasa Fitur Modern

Dokumen ini melacak seluruh gambar placeholder dan status kelengkapannya di dalam draf buku LaTeX (`BookTEX/chapters/`). Berdasarkan audit sistematis pada 8 Juli 2026, status pembagian gambar dibagi menjadi dua kelompok: **Gambar yang Benar-Benar Hilang** (belum dibuat berkasnya) dan **Teks Sisa Konversi** (sudah dibersihkan).

---

## 1. Daftar Gambar yang Benar-Benar Hilang (Missing Figures)
*Gambar-gambar berikut belum memiliki berkas gambar di folder `BookTEX/figures/` dan belum dipasang di dalam berkas bab `.tex`.*

| Bab | Label Placeholder | Baris Asal di `.tex` | Rencana Berkas Gambar | Deskripsi Rencana Visual |
|---|---|---|---|---|
| **Bab 03** | GAMBAR 3.4 | 115 | `ch03-fig-4.png` | Q-Q plot efek transformasi Box-Cox pada data harga yang menceng |
| **Bab 03** | GAMBAR 3.5 | 155 | `ch03-fig-5.png` | Histogram perbandingan distribusi data umur kontinu sebelum & sesudah dipetakan menjadi kelompok interval diskrit |
| **Bab 03** | GAMBAR 3.6 | 179 | `ch03-fig-6.png` | Skema scaling (MinMax vs Standard) yang menormalkan rentang angka antar dimensi fitur |
| **Bab 03** | GAMBAR 3.7 | 215 | `ch03-fig-7.png` | Grafik batang komparatif performa model k-NN & SVM vs Random Forest pasca-standardisasi |
| **Bab 07** | GAMBAR 7.6 | 331 | `ch07-fig-6.png` | Plot shrinkage path koefisien fitur pada regresi LASSO seiring peningkatan nilai penalti L1 |
| **Bab 08** | GAMBAR 8.6 | 433 | `ch08-fig-6.png` | Plot visualisasi 3D ke 2D komparasi ruang laten linier PCA bersanding dengan dimensi non-linier Autoencoder |
| **Bab 09** | GAMBAR 9.X | 269 | `ch09-fig-X.png` | Skema alur kebocoran atribut sensitif ke dalam model melalui korelasi fitur proksi & dimensi embedding |
| **Bab 09** | GAMBAR 9.8 | 315 | `ch09-fig-8.png` | Diagram integrasi Metadata Data Card dan Silsilah Fitur (feature lineage) pada Feature Store |
| **Bab 09** | GAMBAR 9.5 | 368 | `ch09-fig-5.png` | Diagram batang perbandingan skor metrik baseline dengan skor setelah tiap kelompok fitur dicabut (shuffled/dropped) |
| **Bab 11** | GAMBAR 11.6 | 247 | `ch11-fig-6.png` | Skema arsitektur perbandingan aliran gradien pada feature extraction beku (frozen), full fine-tuning, dan PEFT |
| **Bab 11** | GAMBAR 11.5 | 278 | `ch11-fig-5.png` | Skema representasi perbedaan batasan vektor sparse vs dense |
| **Bab 12** | GAMBAR 12.4 | 273 | `ch12-fig-4.png` | Heatmap visualisasi MFCC yang memampatkan rentang frekuensi suara |
| **Bab 16** | GAMBAR 16.5 | 191 | `ch16-fig-5.png` | Bar chart perbandingan performa metrik evaluasi antara baseline fitur manual, ekstraksi murni AutoFE, & kurasi manusia |

---

## 2. Catatan Pembersihan Teks Sisa Konversi (Cleaned Leftover Placeholders)
*Baris-baris berikut sebelumnya berisi teks mentah sisa konversi Markdown `{[}GAMBAR X.Y: ...{]}` padahal gambar tersebut telah terpasang rapi dengan `\begin{figure}` dan `\includegraphics` di bagian lain bab tersebut. Seluruh teks sisa ini telah berhasil **dibersihkan sepenuhnya** dari naskah `.tex`.*

- **Bab 02 (Baris 237):** `{[}GAMBAR 2.4...{]}` — *Dibersihkan*. Gambar asli sudah terpasang di baris 98 (`ch02-fig-4.png`).
- **Bab 05 (Baris 204):** `{[}GAMBAR 5.7...{]}` — *Dibersihkan*. Gambar asli sudah terpasang di baris 177 (`ch05-fig-7.png`).
- **Bab 05 (Baris 238):** `{[}GAMBAR 5.5...{]}` — *Dibersihkan*. Gambar asli sudah terpasang di baris 117 (`ch05-fig-5.png`).
- **Bab 06 (Baris 397):** `{[}GAMBAR 6.4...{]}` — *Dibersihkan*. Gambar asli sudah terpasang di baris 230 (`ch06-fig-4.png`).
- **Bab 07 (Baris 162):** `{[}GAMBAR 7.4...{]}` — *Dibersihkan*. Gambar asli sudah terpasang di baris 82 (`ch07-fig-4.png`).
- **Bab 07 (Baris 214):** `{[}GAMBAR 7.5...{]}` — *Dibersihkan*. Gambar asli sudah terpasang di baris 133 (`ch07-fig-5.png`).
- **Bab 08 (Baris 329):** `{[}GAMBAR 8.5...{]}` — *Dibersihkan*. Gambar asli sudah terpasang di baris 248 (`ch08-fig-5.png`).
- **Bab 09 (Baris 227):** `{[}GAMBAR 9.1...{]}` — *Dibersihkan*. Gambar asli sudah terpasang di baris 32 (`ch09-fig-1.png`).
- **Bab 10 (Baris 360):** `{[}GAMBAR 10.6...{]}` — *Dibersihkan*. Gambar asli sudah terpasang di baris 287 (`ch10-fig-6.png`).
- **Bab 12 (Baris 181):** `{[}GAMBAR 12.1...{]}` — *Dibersihkan*. Gambar asli sudah terpasang di baris 73 (`ch12-fig-1.png`).
- **Bab 12 (Baris 207):** `{[}GAMBAR 12.1...{]}` — *Dibersihkan*. Gambar asli sudah terpasang di baris 73 (`ch12-fig-1.png`).
- **Bab 13 (Baris 537):** `{[}GAMBAR 13.6...{]}` — *Dibersihkan*. Gambar asli sudah terpasang di baris 265 (`ch13-fig-6.png`).
- **Bab 15 (Baris 463):** `{[}GAMBAR 15.5...{]}` — *Dibersihkan*. Gambar asli sudah terpasang di baris 276 (`ch15-fig-5.png`).
- **Bab 17 (Baris 365):** `{[}GAMBAR 17.6...{]}` — *Dibersihkan*. Gambar asli sudah terpasang di baris 290 (`ch17-fig-6.png`).

---

## 3. Instruksi Tindak Lanjut untuk Tim Penulis
1. Buat berkas-berkas gambar pendukung yang terdaftar di **Seksi 1** dengan skema *monokromatik/grayscale* yang kontras untuk media cetak B5.
2. Tempatkan berkas gambar baru tersebut ke dalam direktori `BookTEX/figures/`.
3. Pasang gambar tersebut di lokasi naskah `.tex` yang bersangkutan dengan menyisipkan blok lingkungan gambar LaTeX standar berikut:
   ```latex
   \begin{figure}[htbp]\centering
   \includegraphics[width=\linewidth,height=0.72\textheight,keepaspectratio]{chXX-fig-Y}
   \caption{Judul Gambar Deskriptif}
   \label{fig:chXX-fig-Y}
   \end{figure}
   ```
