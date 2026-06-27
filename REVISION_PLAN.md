# Rencana Revisi Draf 2 — Buku Rekayasa Fitur

Disusun ulang 27 Juni 2026 berdasarkan audit draf 1 (17 bab, 128 subbab) dan arahan Bu Fatma (26–27 Juni 2026).
Dokumen lama dibuang karena pemetaan babnya mengikuti outline usang (Bab 5/6/9/14/16 tertukar).

---

## 1. Status draf 1

- 161 halaman, 51.735 kata (tanpa gambar/figure/tabel).
- 17 bab, 128 subbab. Seluruh subbab sudah dicek 1-per-1 dengan `resources/` → topik cocok.
- Placeholder gambar sudah terpasang (5–9 per bab), rumus block sudah ditambah (≈3–6 per bab).
- Belum lewat tahap review mana pun; gaya bahasa masih perlu dirapikan.

---

## 2. Pemetaan bab yang benar (acuan kerja)

| Bab | Tema | Gambar (placeholder) | Rumus block |
|---|---|---|---|
| 1 | Data, Atribut, Fitur, Representasi | 8 | 4 |
| 2 | Fit/Transform, Pipeline, Data Leakage | 8 | 3 |
| 3 | Skala & Distribusi (numerik kontinu) | 7 | 5 |
| 4 | Variabel Kategorikal & Ordinal | 8 | 4–5 |
| 5 | Missing Values & Outlier | 8 | 6 |
| 6 | Pembentukan Fitur Turunan (rasio, selisih, interaksi, agregasi, domain, datetime) | 8 | 4 |
| 7 | Seleksi Fitur (relevansi, filter, wrapper, embedded) | 6 | 2–3 |
| 8 | Reduksi Dimensi (PCA, NMF, t-SNE/UMAP, autoencoder) | 7 | 4 |
| 9 | Evaluasi Kualitas Fitur (importance, SHAP, ablation, etika) | 8 | 3–4 |
| 10 | Runtun Waktu (lag, rolling, FFT, validasi temporal) | 7 | 4–5 |
| 11 | Teks & NLP (klasik → embedding → LM) | 6 | 3–4 |
| 12 | Citra & Audio | 6 | 3–4 |
| 13 | Graf & Spasial | 9 | 4 |
| 14 | Data Multimodal (fusion, joint embedding) | 7 | 4 |
| 15 | Model Terlatih / Transfer Learning | 9 | 4–5 |
| 16 | AutoFE & LLM-Assisted FE (DFS, AutoML, CAAFE, HITL) | 5 | 1 |
| 17 | Rekayasa Fitur dalam Produksi | 7 | 2–3 |

---

## 3. Todolist pekerjaan berikutnya

### A. Konten yang masih kurang
- [ ] **Gambar fisik** — semua masih placeholder teks, belum ada satu pun diagram nyata. (Pekerjaan terbesar; target ~5–7 jadi gambar per bab.)
- [ ] **Tambah rumus Bab 16** (baru 1) dan cek mutu narasi rumus di seluruh bab ("Di mana X adalah…").
- [ ] **Audit kelengkapan `resources/`** — pastikan external search merata, terutama topik baru (foundation models, SSL, feature store, multimodal) yang kemarin kena rate limit.

### B. Gaya bahasa
- [ ] Sapu **slop AI + "bahasa aneh"** di seluruh draf (pakai skill `stop-slop-id`). Larang kata: krusial, penting diingat, kesimpulannya, lanskap, dll.
- [ ] Pastikan numbered/bulleted list dipakai untuk langkah, komparasi, dan karakteristik (sebagian sudah, perlu disisir).

### C. Tahap review pipeline (TRACK 1 — belum dijalankan sama sekali)
Urutan: Outline → Compilation → Brief → Writer → **Draft (selesai)** → di bawah ini.
- [ ] **Technical Review** per subbab (kebenaran konsep, rumus, istilah).
- [ ] **Editorial Review** per subbab (alur, kejelasan, gaya).
- [ ] **Human Approval per subbab** (acc Bu Fatma / penulis sebelum lanjut).
- [ ] **Redundancy / Transition Review** (hapus pengulangan antar subbab, perbaiki transisi).

### D. Perbaikan proses untuk draf 2
- [ ] **Pisah model**: writer pakai Gemini; gather, review, dan tugas lain boleh model lain (hindari rate limit OpenRouter–Gemini saat paralel).
- [ ] **Pisah step**: kumpulkan bahan selengkapnya **dulu** untuk semua bab (terutama topik baru) sebelum menulis ulang.

---

## 4. Urutan eksekusi yang disarankan

1. Audit + lengkapi `resources/` (gather dulu, model non-Gemini).
2. Sapu gaya bahasa per bab (`stop-slop-id`).
3. Lengkapi rumus (Bab 16) + narasi rumus.
4. Technical Review → Editorial Review → Human Approval per subbab.
5. Redundancy/Transition Review lintas bab.
6. Produksi gambar fisik dari placeholder (paralel, bisa dimulai kapan saja).
