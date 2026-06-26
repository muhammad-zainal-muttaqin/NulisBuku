# Rekayasa Fitur Modern: Representasi Data untuk Machine Learning dan Deep Learning

**Outline / Rencana Buku**

> **Format & skala:** buku praktis dan aksesibel, ~300 halaman B5. Kedalaman teknis dan kode lengkap ditempatkan di repositori pendamping; buku menekankan intuisi, *kapan/mengapa/trade-off*, dan panduan keputusan. Model hybrid: buku = sumber kanonik (apa & mengapa), repo = implementasi (bagaimana).
>
> **Kebijakan bahasa:** istilah teknis mapan dipertahankan dalam bahasa Inggris (*machine learning, deep learning, feature, embedding, pipeline, leakage*). Kosakata penghubung dan konseptual diterjemahkan. Pasangan inti yang konsisten sepanjang buku: **representasi yang dirancang manusia** ↔ **representasi yang dipelajari mesin** (designed by human ↔ learned by machine). Agen eksplisit *manusia/mesin* dipertahankan; hindari bentuk telanjang *dirancang/dipelajari*.

---

## Konsep Inti & Posisi Buku

Benang merah buku: **spektrum dirancang manusia → dipelajari mesin**. Rekayasa fitur tidak hilang di era deep learning—bentuknya bergeser dari representasi yang dirancang (oleh manusia, baik manual maupun otomatis di dalam pipeline) ke representasi yang dipelajari (oleh model), hingga pendekatan hybrid era pretrained/foundation model. Spektrum ini ditegakkan terutama oleh *struktur* buku — urutan bagian bergerak dari yang dirancang ke yang dipelajari — dan **disebut eksplisit jarang saja** (terutama Bab 1 untuk mendefinisikannya dan Bab 17 untuk menutupnya). Di subbab lain, biarkan struktur yang berbicara; mengulang label spektrum di tiap subbab justru menumpulkannya.

> **Catatan istilah:** dipilih "dirancang manusia ↔ dipelajari mesin" (bukan "manual ↔ terlatih", dan bukan bentuk telanjang "dirancang ↔ dipelajari"). Alasannya: (1) yang dilatih adalah *model*, bukan representasinya — representasi *dipelajari mesin*; (2) "manual" keliru menyiratkan kerja tangan tak sistematis, padahal banyak fitur rekayasa dihasilkan otomatis di dalam pipeline; (3) agen eksplisit *manusia/mesin* wajib karena bentuk pasif telanjang "dipelajari" cenderung terbaca "dipelajari oleh kita", padahal pembelajarnya adalah mesin. Sumbu ini simetris, menonjolkan peran manusia, dan tidak ambigu. *(Catatan: frasa Indonesia di sini perlu diperiksa penutur asli.)*

Pembeda dari buku lain: bukan satu bab preprocessing, melainkan rujukan ringkas-namun-luas yang jujur memasukkan DL sebagai pergeseran bentuk feature engineering. Penekanan pada representasi, transformasi, dan seleksi; bukan pembersihan data manual. Nilai di era LLM: menekankan *kapan/mengapa/trade-off*, bukan sekadar *how-to*.

### Benang merah buku (disinggung saat relevan, bukan boilerplate)

Buku punya benang merah, tetapi keduanya **disinggung hanya bila benar-benar relevan**, bukan distempel ke tiap subbab:

1. **Spektrum dirancang manusia → dipelajari mesin** — ditegakkan oleh *struktur* buku dan didefinisikan di Bab 1. **Disebut eksplisit jarang saja:** pada dasarnya hanya Bab 1 (definisi) dan Bab 17 (penutup), plus paling banter satu-dua titik balik paling penting (mis. saat representasi pertama kali menjadi *dipelajari mesin*). Di subbab lain, jangan sebut spektrumnya.
2. **Praktik pipeline yang benar** — rumahnya di **Bab 2**; di bab lain disinggung **jarang saja**, hanya bila teknik itu memang berisiko leakage / training–serving skew. Pembahasan mendalam tetap di Bab 2 (ditinjau lagi di Bab 17); buku ini tentang feature engineering, bukan MLOps.

---

## Skala & Anggaran Halaman

| | |
|---|---|
| Target | ~300 halaman B5 (toleransi +5–10% di tingkat buku, ≈330 hlm) |
| Target kata | ~52.000 kata (Bahasa Indonesia) — lihat catatan anggaran kata |
| Jumlah bab | 17 bab (1 pengantar + 15 inti + 1 penutup) |
| Rata-rata per bab | ~17 halaman B5 (≈3.050 kata) — bervariasi: Bab 1 lebih ringan, bab inti tipe-data & ML modern lebih padat |
| Template bab | ringkas (8 elemen, lihat bawah) — bukan template teori berat |
| Kode panjang | **di repositori, bukan di buku** — aturan keras, lihat catatan kepadatan |

> **Catatan anggaran kata:** ~300 hlm B5 × ~240 kata/hlm penuh teks ≈ ~72.000 kata bila 100% teks; menyisihkan 25–30% ruang untuk gambar/tabel/heading menyisakan ~50.000–54.000 kata prosa (target ~52.000, Bahasa Indonesia). Draf kerja dalam bahasa Inggris ditargetkan ~45.000 kata (Indonesia memuai ~1,1–1,25× terhadap Inggris). Rincian pipeline ada di dokumen rencana pipeline.

---

## STRUKTUR BUKU

### BAGIAN I — FONDASI

**Bab 1. Dari Data Mentah ke Representasi Model**
Data, atribut, fitur, representasi. Peran fitur dalam ML. Kapan representasi dirancang manusia vs. dipelajari mesin — pengenalan **spektrum dirancang manusia → dipelajari mesin** sebagai kerangka buku. Mitos "feature engineering sudah mati di deep learning". **Dari pertanyaan prediksi ke tabel pembelajaran:** unit observasi, target & horizon prediksi, waktu prediksi, dan batas ketersediaan informasi sebuah fitur (banyak "kesalahan FE" sebenarnya kesalahan konstruksi sampel). **Peta struktur representasi:** vektor/matriks fitur, sekuens, grid/tensor, himpunan, graf, multimodal — agar pembaca tidak menganggap semua representasi berbentuk $X\in\mathbb{R}^{n\times d}$. Gambaran pipeline.
*Studi kasus: data transaksi sederhana → matriks fitur (menerapkan definisi unit/target lebih dulu).*

**Bab 2. Pipeline, Validasi, dan Data Leakage**
*(fondasi & rumah **praktik pipeline yang benar** — dirujuk seperlunya, jarang, di bab lain)*
Fit/transform; pipeline sebagai kontrak training–inference. Transformer yang reusable; serialization; reproducible random state. Taksonomi leakage (target, kontaminasi train-test, temporal, antar-kelompok). Mengapa leakage lahir di tahap feature engineering. Split yang benar: random, group, temporal. Pipeline di dalam cross-validation. Kesalahan umum mahasiswa.
*Studi kasus: pipeline valid vs. pipeline yang bocor.*

### BAGIAN II — TRANSFORMASI DATA TABULAR

**Bab 3. Representasi Fitur Numerik**
Skala & distribusi. Standardization, min-max, robust scaling, power & quantile transform, clipping, binning. Model yang sensitif vs. tidak sensitif terhadap skala.
*Studi kasus: pengaruh transformasi pada k-NN, SVM, tree-based.*

**Bab 4. Representasi Fitur Kategorikal**
Nominal/ordinal/high-cardinality. One-hot, ordinal, frequency, target encoding (+risiko leakage), hashing, entity embedding (jembatan ke representasi yang dipelajari mesin). Unseen categories.
*Studi kasus: perbandingan encoding pada kategori besar.*

**Bab 5. Missing Values & Outlier (Reproducible, Berbasis Pipeline)**
*(penanganan yang reproducible dan berbasis pipeline — "otomatis" berarti tidak disunting baris-per-baris, bukan diterapkan tanpa inspeksi, diagnostik, dan penilaian)*
Mekanisme missingness (MCAR/MAR/MNAR) secukupnya — inspeksi mendahului otomasi. Imputasi sebagai komponen pipeline (transformer yang di-*fit* & reproducible, bukan koreksi manual sekali jalan). Missing indicator. Outlier: deteksi vs. penanganan, transformasi robust. Batas data cleaning ↔ feature engineering.
*Studi kasus: pipeline imputasi & penanganan robust yang reproducible — di-fit pada train saja, terinspeksi, leakage-safe.*

**Bab 6. Pembentukan Fitur Turunan**
Rasio, selisih, interaksi, polynomial, agregasi, fitur berbasis kelompok & domain, fitur tanggal/waktu & siklik. **Fitur relasional & event-log:** join satu-ke-banyak, duplikasi akibat join ceroboh, *point-in-time / as-of join*, agregasi riwayat event menjadi fitur tingkat-entitas yang hanya memakai data sebelum waktu prediksi (jembatan ke feature synthesis otomatis, Bab 16). Risiko ledakan fitur; validasi manfaat fitur baru.
*Studi kasus: fitur turunan dari data transaksi/kesehatan/pendidikan.*

### BAGIAN III — SELEKSI & REDUKSI DIMENSI

**Bab 7. Seleksi Fitur**
*(gabungan: dasar + metode)*
Relevansi vs. redundansi, curse of dimensionality. Filter (korelasi, MI, chi-square), wrapper (RFE, sequential), embedded (LASSO, tree-based, Boruta). Stabilitas seleksi; nested validation.
*Studi kasus: perbandingan metode seleksi pada satu dataset.*

**Bab 8. Reduksi Dimensi & Representasi Laten**
PCA, SVD/truncated SVD, NMF, manifold learning (t-SNE, UMAP), autoencoder. Visualisasi vs. preprocessing model. Risiko penggunaan yang keliru.
> **Batas eksplisit dengan Bab 15 (cross-reference dua arah):** Bab 8 = *kompresi tanpa-supervisi atas matriks fitur Anda sendiri* (PCA, SVD, NMF, autoencoder). Bab 15 = *representasi semantik yang ditransfer dari data lain/lebih besar* (pretrained embedding). Pembedaan "data Anda sendiri vs. transfer dari luar" — bukan sekadar "statistik vs. neural" — agar autoencoder (neural, tapi tetap di Bab 8) tidak menjadi pengecualian yang membingungkan.
*Studi kasus: PCA & autoencoder untuk data berdimensi tinggi.*

**Bab 9. Evaluasi Kualitas Fitur**
**Apa yang membuat sebuah fitur baik?** Kualitas lebih luas daripada importance prediktif: ketersediaan saat inference, stabilitas lintas waktu/populasi, sensitivitas terhadap galat pengukuran, biaya komputasi/penyimpanan/latensi, interpretabilitas, robustness terhadap shift. Baseline; ablation study; permutation & model-based importance; SHAP untuk diagnosis. Stability across folds; importance ≠ kausalitas. **Informasi sensitif & fitur proxy:** atribut sensitif langsung, proxy (kode pos, tipe perangkat), embedding yang menyimpan informasi pribadi, efek menghapus vs. mempertahankan atribut terlindungi terhadap fairness, minimisasi data — "meningkatkan akurasi" ≠ "layak dipakai" (ringkas, bukan bab etika; muncul lagi sebagai callout di Bab 17). Dokumentasi keputusan fitur.
*Studi kasus: ablation terhadap beberapa kelompok fitur.*

### BAGIAN IV — REKAYASA FITUR BERDASARKAN JENIS DATA

**Bab 10. Deret Waktu & Data Sensor**
**Konstruksi sampel temporal** (windowing membentuk *sampel* pembelajaran): panjang lookback, stride, horizon prediksi, panjang target-window, penyelarasan input↔target, window kausal vs. terpusat, dependensi antar-window tumpang-tindih, sampling tak teratur/resampling. **Lalu** fitur lag & rolling stats (dihitung *di dalam* window), difference, trend & seasonality. Fitur domain frekuensi (FFT) secukupnya. Validasi temporal (anti look-ahead; leakage spesifik-modalitas: window tumpang-tindih melintasi batas split). Fitur untuk model klasik vs. input sekuensial (RNN/LSTM/Transformer).
*Studi kasus: prediksi deret waktu multivariat.*

**Bab 11. Teks & Dokumen**
Klasik: tokenisasi, bag-of-words, n-gram, TF-IDF. Pergeseran ke dipelajari mesin: word, contextual, sentence, document embedding. Pretrained LM sebagai feature extractor; fine-tuning vs. feature extraction.
*Studi kasus: klasifikasi dokumen — TF-IDF vs. contextual embedding.*

**Bab 12. Citra & Audio**
*(gabungan dipertahankan: keduanya berbagi pola pretrained-encoder; namun representasi & isu pipeline masing-masing dibahas terpisah di dalam bab)*
Citra: normalisasi, augmentasi, handcrafted (HOG) → CNN feature extractor, pretrained vision model, image embedding, patch. Audio: waveform, spectrogram, MFCC, chroma → pretrained audio encoder, audio embedding, agregasi sepanjang waktu.
> **Audio sebagai miniatur spektrum dirancang manusia → dipelajari mesin:** spectrogram/Mel/MFCC = ujung *dirancang manusia* (representasi rancangan tangan, di sini "spectrogram-sebagai-citra" berguna sebagai jembatan visual). Encoder *raw waveform* (wav2vec 2.0, HuBERT) = ujung *dipelajari mesin* dan merupakan pendekatan SOTA modern. Hindari menyajikan spectrogram-sebagai-citra sebagai satu-satunya jembatan — itu framing pra-2018; sebutkan eksplisit pemrosesan raw waveform sebagai sisi modern.
*Studi kasus: handcrafted vs. deep features (citra & audio).*

**Bab 13. Data Spasial & Graf**
*(dipisah dari multimodal — keduanya butuh ruang sendiri agar tidak superfisial)*
Spasial: koordinat sebagai fitur, sistem referensi, jarak & kedekatan, neighborhood features, autokorelasi spasial, leakage spasial & spatial cross-validation. Graf: degree/centrality/clustering, neighborhood aggregation, path-based features, node embedding (Node2Vec), GNN sebagai representation learner, leakage pada graf.
*Studi kasus: prediksi berbasis lokasi (validasi spasial) & klasifikasi node.*

**Bab 14. Data Multimodal**
*(bab tersendiri — bukan tempelan)*
Definisi & alignment antar modalitas; sinkronisasi waktu. **Strategi fusion: early / intermediate / late, serta di tingkat fitur vs. keputusan** (digabung — keduanya soal *di mana* penggabungan terjadi). Feature concatenation & dimensionality balancing. Missing modality. Cross-modal & joint embedding. Multimodal pretrained model.
*Studi kasus: menggabungkan tabular + citra/teks/sensor dalam satu pipeline.*

### BAGIAN V — REKAYASA FITUR DALAM ML MODERN

**Bab 15. Representasi yang Dipelajari Mesin & Pretrained Model**
*(ujung dipelajari mesin dari spektrum, dibuat praktis)*
Embedding & spektrum adaptasi: dari frozen extractor → partial → full fine-tuning (ringkas: static vs. contextual sudah di Bab 11). Embedding/feature bank & similarity metrics. Evaluasi kualitas embedding; risiko domain shift. Batas dengan Bab 8 (representasi yang ditransfer vs. kompresi data sendiri). Apakah DL menghapus kebutuhan FE: learned vs. handcrafted. Input representation, tokenization, augmentation (FE yang bertahan di dalam DL). **Deep learning untuk data tabular:** tabular transformer (FT-Transformer, TabNet), deep tabular net sebagai feature extractor; kapan menang/kalah dari gradient boosting; kaitan dengan entity embedding (Bab 4). Model hybrid (engineered features sebagai input tambahan).
*Studi kasus: pretrained model sebagai feature extractor + model hybrid (learned + engineered).*

**Bab 16. Rekayasa Fitur Otomatis & Kolaborasi Manusia–AI**
*(otomasi tetap dirancang manusia — diarahkan manusia, bukan dipelajari mesin)*
Automated feature generation: Deep Feature Synthesis & ruang pencarian (atas data relasional/event, kaitan ke Bab 6); AutoML & pipeline fitur otomatis. GenAI untuk usulan fitur; risiko fitur tak bermakna (plausibel tapi spurious). Human-in-the-loop: validasi & kurasi fitur usulan mesin — penilaian perancang tetap esensial; automated FE itu otomatis namun tetap *dirancang manusia*.
*Studi kasus: fitur otomatis (DFS/AutoFE) yang disaring validasi manusia pada data relasional, diukur terhadap baseline.*

> Catatan: bekas Bab 15 (yang menyerap tiga topik) kini dipecah menjadi Bab 15 (representasi yang dipelajari mesin) dan Bab 16 (rekayasa fitur otomatis), sesuai masukan kolega — dua *arc* intelektual yang berbeda. Disiplin kepadatan tetap berlaku: kode dijaga minimal (*signature snippet* terbatas, lihat aturan kepadatan), halaman dipakai untuk diagram arsitektur + diskusi why/trade-off. Lihat juga batas eksplisit dengan Bab 8 (kompresi data sendiri vs. transfer dari luar).

### BAGIAN VI — PENUTUP

**Bab 17. Sintesis: Merancang Pipeline & Prinsip yang Bertahan Lama**
*(gabungan dari rancangan + prinsip — dua paruh yang jelas, bukan dilebur)*
**Paruh A — Kerangka perancangan:** dari tujuan prediksi → **unit observasi → target → strategi split** (tulang punggung yang sudah disiapkan di Bab 1) → sumber fitur → transformasi → seleksi → baseline → evaluasi → pipeline final. Konsistensi training–inference, training-serving skew, schema validation, versioning transformasi, drift (ringkas). Decision framework lintas tipe data.
**Paruh B — Prinsip yang bertahan lama (dua kelompok terpadu):** (I) mulai dari masalah bukan teknik; fitur harus tersedia saat inference; transformasi mengikuti pembagian data (plus callout ringkas privasi/proxy, rekap Bab 9). (II) fitur kompleks tidak selalu lebih baik dan validasi > jumlah fitur; representasi yang dirancang manusia & yang dipelajari mesin saling melengkapi; arah ke depan.
*Studi kasus: merancang pipeline dari nol untuk beberapa skenario.*

---

## LAMPIRAN

- **Lampiran A.** Peta pemilihan teknik (tipe data × jenis model × ukuran data × kebutuhan interpretabilitas)
- **Lampiran B.** Checklist pencegahan data leakage (split, transformasi, seleksi, CV, temporal, group, inference)
- **Lampiran C.** Template dokumentasi fitur (nama, definisi, sumber, formula, waktu ketersediaan, risiko leakage, versi)
- **Lampiran D.** Glosarium (Indonesia–Inggris, definisi ringkas)
- **Lampiran E.** **Matriks Dataset × Bab** — daftar dataset kurasi, di bab mana dipakai, dan untuk axis apa. Alat perencanaan reuse saat menulis; sekaligus tabel bagi mahasiswa ("dataset ini muncul di Bab 4, 6, 9 — bagus untuk melihat satu data sepanjang pipeline tabular").
- **Lampiran F.** **Proyek Capstone (lintas-bab)** — **3 capstone lengkap** yang sudah dirancang penuh (sebaiknya beda bentuk: mis. tabular, sekuens/teks, multimodal — sekaligus contoh keragaman), tiap capstone ditandai bab prasyaratnya. **Plus kerangka capstone** bagi mahasiswa yang ingin merancang/mengadaptasi capstone sendiri. Mini-proyek per bab melayani kuliah; capstone melayani peneliti.

> **Kerangka capstone wajib mewariskan disiplin buku:** validasi anti-leakage, perbandingan/ablation wajib, dan pertanyaan refleksi spektrum *dirancang manusia → dipelajari mesin*. Ini yang menjaga capstone rancangan-mahasiswa-sendiri tetap seketat tiga capstone contoh.

> **Catatan footprint cetak (penting untuk anggaran halaman):** seluruh lapisan hybrid (mini-proyek, dataset kurasi, rubrik, capstone) **berada di repositori**, bukan di tubuh buku. Di buku cetak, Lampiran E & F (dan mini-proyek tiap bab) hanya berupa **penunjuk** — total ~2–3 halaman (≈1 halaman per lampiran). Konsekuensi tambahan: proyek & dataset dapat **diperbarui/ditambah pasca-terbit tanpa cetak ulang** — rumah yang tepat karena dataset, versi library, dan ide proyek bergeser lebih cepat daripada buku cetak. Buku = indeks stabil; repo = konten hidup.

> **Peta dependensi / routing (di depan buku):** diagram kecil "selalu baca Bab 1–2 dulu → lompat ke bab tipe-data Anda → baca Bab 9 sebelum melaporkan hasil." Membuat fungsi *router* aman: mahasiswa yang hanya membaca satu bab tipe-data tidak menghasilkan kerja yang bocor/tak tervalidasi. Bab 2 (pipeline/leakage) & Bab 9 (evaluasi fitur) adalah prasyarat untuk semua jalur.

---

## FORMAT STANDAR SETIAP BAB (ringkas — versi praktis)

1. Tujuan pembelajaran
2. Ilustrasi masalah
3. Konsep utama + intuisi
4. **Kapan / mengapa / trade-off** *(inti bab)*
5. **Callout — hanya bila relevan, bukan wajib tiap subbab:** (a) posisi pada spektrum *dirancang manusia → dipelajari mesin* **sangat jarang** — default-nya tidak disebut, hanya bila subbab ini memang titik balik utama; (b) praktik pipeline yang benar bila ada risiko leakage / konsistensi training–inference nyata (termasuk *leakage spesifik-modalitas* di bab tipe-data); (c) *interaksi dengan keluarga model* bila keputusan bergantung padanya. Tulis sebagai klausa singkat yang menyatu dengan prosa, bukan kotak berlabel yang memutus alur.
6. Studi kasus singkat
7. Kesalahan umum
8. Ringkasan keputusan + tautan notebook & materi pendamping
9. **Latihan & pertanyaan konseptual** — di tubuh buku, di akhir bab (bagian dari paket pedagogis bab)
10. **Referensi & bacaan lanjut** — di akhir bab
11. **Mini-proyek bab** — di buku hanya *penunjuk ringkas* (tugas + axis + ke repo); menu lengkap, dataset, rubrik berada di repositori (lihat "Desain Mini-Proyek")

> Notebook **disebut, bukan dijelaskan**: prosa menunjuk notebook bab tempat sebuah konsep didemonstrasikan (seperti rujukan gambar), uraian kode ada di repo. Paket pedagogis lengkap per bab (tujuan, pengingat prasyarat, contoh terpandu, tabel/diagram keputusan, callout, ringkasan, latihan, referensi) didefinisikan di dokumen rencana pipeline (§5) dan **dirakit di tingkat bab, bukan per-subbab**. Formulasi matematis dijaga minimal dan opsional; kode lengkap di repositori (kecuali *signature snippet* terbatas, lihat aturan kepadatan).

### Disiplin kepadatan (aturan global)

Untuk menjaga cakupan-luas tetap muat di halaman kecil tanpa berubah menjadi glosarium:
- **Default tanpa blok kode sebagai penjelasan.** Cukup nama fungsi/komponen dan alurnya dalam prosa; *one-liner* inline boleh (mis. `StandardScaler().fit(X_train)`). **Pengecualian terbatas:** *signature snippet* pendek (≤ ~5 baris, ~1 per bab) untuk menunjukkan *bentuk* pemanggilan — **disalin dari notebook bab yang sudah terverifikasi**, bukan ditulis di prosa. Penulis hanya menaruh placeholder `[KODE: ...; sumber: notebook bab]`; kode asli diisi saat perakitan bab. Selebihnya kode → repositori.
- Halaman dibelanjakan untuk **diagram arsitektur** dan **diskusi why/trade-off**, bukan listing. (Catatan: diagram pun memakan ruang — di B5 satu diagram baik ≈ ⅓–½ halaman; tetap lebih berharga daripada blok kode.)
- Bab terpadat (mis. Bab 13, 15) adalah penguji aturan ini; bila kepadatan tak tertahankan, pisahkan bab (sebagaimana bekas Bab 15 telah dipecah menjadi Bab 15 & 16), bukan dengan memadatkan teks hingga dangkal.

---

## DESAIN MINI-PROYEK (per bab)

Tujuan ganda buku: (a) **router** bagi mahasiswa peneliti — diarahkan ke bab tertentu sesuai proyek ML/DL mereka; (b) bahan **mata kuliah pilihan**. Mini-proyek dirancang agar **jalur tiap mahasiswa berbeda** namun **dinilai dengan satu rubrik** — cocok untuk kelas 30+ mahasiswa sekaligus tahan terhadap contek/LLM (hasil bergantung pilihan & perilaku data mereka sendiri).

### Struktur tetap setiap mini-proyek
1. **Tugas (tetap):** satu jenis tugas + satu aturan evaluasi yang sama untuk semua.
2. **Dataset:** **2–3 dataset kurasi** yang sudah kami siapkan (bersih, terdokumentasi, siap-tugas — mahasiswa fokus ke representasi, bukan cleaning). **Bawa-data-sendiri** selalu terbuka (jalur peneliti). Dataset kurasi **dipakai ulang lintas bab bila cocok** — tidak dipaksakan.
3. **Axis 1 — pilihan representasi/teknik (3–4 opsi):** dipetakan ke spektrum *dirancang manusia → dipelajari mesin* (mis. encoding bersaing; handcrafted vs. pretrained vs. hybrid).
4. **Axis 2 — sudut evaluasi/ablation (2–3 opsi):** dipetakan ke disiplin evaluasi (perbandingan mana yang dijalankan; kelompok fitur mana yang diablasi).
5. **Wajib: perbandingan/ablation** — minimal dua representasi diadu, dilaporkan jujur mana yang menang **dan mengapa** (menanamkan refleks anti-"jatuh cinta pada satu metode").
6. **Pertanyaan refleksi spektrum (tetap):** "di mana masalah *Anda* berada pada kontinum dirancang manusia → dipelajari mesin, dan mengapa?" — jawaban berbeda antar mahasiswa; membandingkannya di kelas *adalah* pelajarannya.
7. **Rubrik (tetap).**

### Ruang divergensi
Minimum 3×2 = **6 jalur** berbeda (hingga 4×3 = 12), sebelum dataset (3 opsi) dan bawa-data-sendiri memperlebarnya. Dua axis = dua benang merah buku yang dilatih langsung (Axis 1 ↔ spektrum, Axis 2 ↔ evaluasi).

### Prinsip
- **Menu, bukan halaman kosong:** opsi konkret menurunkan kelumpuhan pilihan untuk S1; jalur "bawa-data-sendiri" melayani track peneliti.
- **Skeleton tetap, isi variabel** — cermin dari cara bab itu sendiri bekerja.

> Maintenance: lihat **Lampiran E (Matriks Dataset × Bab)** agar pemakaian-ulang dataset tetap disengaja dan terlacak.

---

## MATERI PENDAMPING DIGITAL (REPOSITORI)

Notebook per bab • **dataset kurasi (2–3/bab, siap-tugas)** • template pipeline • custom transformer (reusable) • unit test untuk transformer • contoh schema validation & serialization • contoh ablation • **menu mini-proyek + rubrik** • solusi latihan terpisah • daftar dependensi/environment • diagram pipeline & template diagram yang dapat dipakai ulang.

> **Format eksekusi disarankan:** Quarto atau Jupyter Book — satu sumber → PDF (penerbit) + HTML interaktif + notebook. Menyelesaikan dilema "buku vs. mahasiswa CS yang jarang membaca buku".

---

## STRATEGI PENULISAN (BERTAHAP)

1. **Fondasi:** Bab 1–2, lalu 17 (perancangan) — menetapkan kerangka, spine, & praktik pipeline yang benar.
2. **Tabular:** Bab 3–6.
3. **Seleksi/reduksi/evaluasi:** Bab 7–9.
4. **Tipe data sesuai kepakaran penulis dulu:** dari Bab 10–14 (tulis yang terdekat dengan keahlian lebih awal).
5. **ML modern:** Bab 15–16.
6. **Penutup & lampiran:** lengkapi Bab 17, Lampiran A–D, glosarium, repositori.

---

## CATATAN KONSOLIDASI & REVISI

**Penggabungan agar muat ~150 hlm A5 tanpa kehilangan cakupan:**
- Pipeline + Leakage → **Bab 2**
- Dasar seleksi + Metode seleksi → **Bab 7**
- Citra + Audio → **Bab 12** (berbagi jembatan spectrogram & pretrained-encoder; representasi masing-masing tetap dibahas terpisah)
- Embedding/pretrained + FE-dalam-DL → **Bab 15**; Automated FE → **Bab 16** (dipisah, lihat revisi putaran 3)
- Rancangan pipeline + Prinsip → **Bab 17** (dua paruh yang jelas)
- Data-centric ML diserap ringkas ke Bab 9 & 17

**Revisi dari masukan kolega:**
- Spasial/Graf/Multimodal **tidak lagi satu bab** — dipecah menjadi Bab 13 (Spasial & Graf) dan Bab 14 (Multimodal), karena penggabungan tiga area berbeda menjadi 6–7 hlm terlalu superfisial.
- Terminologi spine diganti: **"dirancang manusia ↔ dipelajari mesin"** menggantikan "manual ↔ terlatih" (lihat Catatan istilah di atas).
- **Praktik pipeline yang benar** berumah di Bab 2; di bab lain disinggung jarang (hanya saat ada risiko leakage nyata), **bukan** callout di tiap bab — agar identitas buku tetap *feature engineering*, bukan MLOps.

**Revisi dari masukan kolega (putaran 2 — risiko eksekusi):**
- **Kepadatan vs. anggaran halaman:** ditetapkan aturan global tanpa-kode-di-teks + toleransi +1–2 hlm/bab; katup tekanan bekas Bab 15 kini benar-benar dijalankan (dipecah jadi Bab 15 & 16 pada putaran 3).
- **Bab 12 (audio):** jembatan "spectrogram-sebagai-citra" tidak lagi disajikan sebagai satu-satunya jembatan; raw-waveform encoder (wav2vec 2.0, HuBERT) disebut eksplisit sebagai ujung *dipelajari mesin* modern. Audio menjadi miniatur spektrum dirancang manusia → dipelajari mesin.
- **Batas Bab 8 ↔ Bab 15:** cross-reference dua arah ditambahkan. Garis batas dirumuskan sebagai *kompresi data sendiri (PCA/SVD/NMF/autoencoder)* vs. *transfer representasi semantik dari luar (pretrained embedding)* — bukan "statistik vs. neural", agar autoencoder tidak menjadi pengecualian.

**Revisi dari masukan kolega (putaran 3 — struktur, cakupan & pipeline):**
- **Bab 15 dipecah** menjadi Bab 15 (Representasi yang Dipelajari Mesin & Pretrained Model) dan Bab 16 (Rekayasa Fitur Otomatis & Kolaborasi Manusia–AI); bekas Bab 16 sintesis menjadi **Bab 17**. **Total kini 17 bab** (sekaligus menyelesaikan ketidakcocokan 16-vs-17 antara outline dan dokumen rencana).
- **Konstruksi sampel pembelajaran** ditambahkan di awal (Bab 1): unit observasi, target & horizon, batas ketersediaan informasi fitur — banyak "kesalahan FE" sebenarnya kesalahan konstruksi sampel; ditarik ke depan, tidak hanya di bab sintesis.
- **Peta struktur representasi** (vektor/sekuens/grid/himpunan/graf/multimodal) di Bab 1, agar Bagian IV–V punya tujuan yang jelas sejak awal.
- **Fitur relasional & point-in-time** (join satu-ke-banyak, as-of join, agregasi event-log) ditambahkan ke Bab 6 — mengisi celah antara agregasi kelompok (Bab 6) dan synthesis otomatis (Bab 16).
- **Konstruksi window temporal dipisah** dari fitur lag/rolling di Bab 10 (window membentuk *sampel*; lag/rolling membentuk *fitur*).
- **Kualitas fitur diperluas** di Bab 9 (ketersediaan saat inference, stabilitas, biaya, latensi — bukan hanya importance) + subbab **privasi/fairness/proxy** ringkas (muncul lagi sebagai callout di Bab 17).
- **Bab 5 di-reframe** dari "Otomatis, Bukan Manual" menjadi "Reproducible, Berbasis Pipeline": otomasi berarti tidak disunting baris-per-baris, bukan diterapkan tanpa inspeksi/diagnostik.
- **Callout berulang** ditambah: *interaksi dengan keluarga model* dan *leakage spesifik-modalitas*.
- **Anggaran kata tetap:** penambahan diimbangi penggabungan (Bab 8 s06+s07, Bab 14 s02+s07, bekas Bab 15 s01–s03, lima prinsip Bab 17 → dua); 127 → 129 subbab, total kata buku tidak berubah (diserap anggaran per-subbab).
- **Penyelarasan pipeline** (provenance pada brief + cek sumber di Technical Review, tahap *Chapter Integrator* + *whole-book coherence*, alur gambar/pedagogi, kontrak notebook yang dapat dikoreksi balik) dicatat di dokumen rencana pipeline.
> *(Frasa Indonesia pada blok-blok baru perlu diperiksa penutur asli.)*

**Penggunaan (memandu desain):** buku berfungsi sebagai (a) *router* bagi mahasiswa peneliti S1 — diarahkan ke bab spesifik sesuai proyek; (b) bahan mata kuliah pilihan. Konsekuensi desain: bab harus modular (dapat dibaca lompat), dengan Bab 2 & 9 sebagai prasyarat universal (lihat peta dependensi); tiap bab punya mini-proyek berstruktur-tetap tapi berhasil-beragam (lihat Desain Mini-Proyek); dataset dikurasi & siap-tugas; ada bank capstone lintas-bab untuk track peneliti.

**Yang dijaga tetap utuh:** fondasi, tabular sebagai inti, evaluasi fitur (Bab 9, sering diabaikan buku lain), dan tipe data bernilai tinggi (deret waktu, teks).
