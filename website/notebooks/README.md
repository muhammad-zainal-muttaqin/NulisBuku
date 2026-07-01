# Notebook Praktik - Rekayasa Fitur Modern

Satu notebook per bab. Tiap notebook punya **dua bagian** sesuai konsep buku:

1. **Section 1 - Demo:** mengimplementasikan *Studi Kasus* bab. Tinggal dijalankan sel demi sel, lalu amati keluarannya (tabel, metrik, plot). Tiap blok ditutup catatan **🔎 Amati**.
2. **Section 2 - Mini Project:** soal + data awal. Mahasiswa mengerjakan sendiri dari nol (tanpa kunci jawaban).

## Tingkat dependensi

| Tingkat | Bab | Cara menjalankan |
|---|---|---|
| **Ringan** | 1–10 (tabular, time-series) | Laptop biasa tanpa GPU. `pip install -r ../../requirements.txt` lalu buka di Jupyter. |
| **Lanjutan** | 11+ (teks, citra, audio, graf, pretrained) | Disarankan **Google Colab** (GPU). Tiap notebook punya sel `%pip install ...` dan badge *Open in Colab*. |

## Menjalankan secara lokal

```bash
pip install -r requirements.txt        # dari root repo
cd website/notebooks
jupyter lab                            # atau: jupyter notebook
```

## Menjalankan di Google Colab

Klik badge **Open in Colab** di sel pertama tiap notebook, atau buka:
`https://colab.research.google.com/github/muhammad-zainal-muttaqin/NulisBuku/blob/main/website/notebooks/<chXX.ipynb>`

## Integrasi dengan buku (Quarto)

Notebook didaftarkan di `website/_quarto.yml` (part *"Notebook Praktik"*) sehingga ikut tampil di website buku. Tiap notebook diberi metadata `execute: { enabled: false }`, jadi `quarto render` hanya **menampilkan output yang sudah tersimpan** dan tidak akan memasang `torch`/`transformers` saat build CI. Alur kerja: jalankan notebook (di Colab/lokal) → simpan beserta output → commit.

## Status

Pilot: **Bab 2** (ringan) dan **Bab 11** (lanjutan/Colab). Bab lain menyusul setelah template ini disetujui.
