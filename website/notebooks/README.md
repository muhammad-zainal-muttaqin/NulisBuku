# Notebook Praktik - Rekayasa Fitur Modern

Satu notebook per bab (Bab 1-17). Tiap notebook punya **dua bagian** sesuai konsep buku:

1. **Section 1 - Demo:** mengimplementasikan *Studi Kasus* bab. Tinggal dijalankan sel demi sel, lalu amati keluarannya (tabel, metrik, plot). Tiap blok ditutup catatan **🔎 Amati**. Section 1 dieksekusi dalam hitungan detik; waktu ~30-60 menit yang diharapkan per bab adalah untuk membaca, menjalankan, dan **menelaah** hasilnya, bukan menunggu komputasi.
2. **Section 2 - Mini Project:** soal + data awal. Mahasiswa mengerjakan sendiri dari nol (tanpa kunci jawaban).

## Kebutuhan

Semua bab memakai *stack* Python standar: **tanpa GPU, tanpa pretrained model, tanpa sel `pip install` khusus**. Bahkan bab modalitas lanjutan (teks, citra, audio, graf, multimodal) tetap ringan karena ekstraksi fitur yang berat sudah **diprakomputasi** dan disimpan sebagai *snapshot* di `data/section1/`. Paket yang diperlukan: `numpy`, `pandas`, `scikit-learn`, `scipy`, `matplotlib`, `pyarrow` (untuk `.parquet`), ditambah `pillow` (Bab 14) dan `networkx` (Bab 13) — semuanya ada di `requirements.txt`.

## Data

Section 1 memuat data secara otomatis lewat pembantu `section_data_dir(name)`:

- **Lokal:** jika folder `data/section1/<name>/` tersedia (mis. saat dijalankan dari dalam repo), berkas dipakai langsung.
- **Colab / tanpa salinan lokal:** berkas diunduh otomatis dari repo GitHub sesuai `manifest.json` tiap bab, lalu di-*cache* ke `_nb_data/`. Tidak perlu mengunggah apa pun secara manual.

Total *snapshot* Section 1 untuk semua bab sekitar 37 MB.

## Menjalankan secara lokal

```bash
pip install -r requirements.txt        # dari root repo
cd website/notebooks
jupyter lab                            # atau: jupyter notebook
```

## Menjalankan di Google Colab

Klik badge **Open in Colab** di sel pertama tiap notebook, atau buka:
`https://colab.research.google.com/github/muhammad-zainal-muttaqin/NulisBuku/blob/main/website/notebooks/<chXX.ipynb>`

Dependensi di atas sudah tersedia di Colab dan data terunduh otomatis, jadi notebook bisa langsung dijalankan tanpa penyiapan tambahan.

## Integrasi dengan buku (Quarto)

Notebook didaftarkan di `website/_quarto.yml` (part *"Notebook Praktik"*) sehingga ikut tampil di website buku. Tiap notebook diberi metadata `execute: { enabled: false }`, jadi `quarto render` hanya **menampilkan output yang sudah tersimpan** dan tidak mengeksekusi ulang saat build. Alur kerja: jalankan notebook (di Colab/lokal) → simpan beserta output → commit.

## Status

- **Section 1 (Demo):** lengkap untuk Bab 1-16; Bab 17 berupa sintesis konseptual (tanpa sel kode).
- **Section 2 (Mini Project):** tiap bab sudah berisi soal + data awal; pengembangan lebih lanjut ditangani asisten.
