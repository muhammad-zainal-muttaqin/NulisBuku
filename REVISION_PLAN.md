# Blueprint Revisi Draf Buku (Sesuai Arahan Bu Fatma)

Dokumen ini merupakan panduan injeksi elemen visual, matematis, dan struktural ke dalam draf prosa (`drafts/*.md`) yang diinstruksikan pada 26/27 Juni 2026.

## 1. Aturan Umum (Mandate)
*   **Gambar (Visual):** Target 5-7 gambar/diagram per bab. Tuliskan dalam format placeholder `[GAMBAR <Nomor Bab>.<Urutan>: <Tipe Gambar> - <Deskripsi Visual>]` (contoh: `[GAMBAR 1.1: Diagram Alur - Perbandingan workflow machine learning klasik vs deep learning]`).
*   **Rumus (Matematis):** Wajib menggunakan *Block Equation* (dibungkus `$$ ... $$`) untuk rumus utama, jangan hanya *inline* (`$ ... $`). Narasikan rumus tersebut ("Di mana X adalah... dan Y adalah...").
*   **Struktur Teks:** Pecah teks panjang (wall of text) menjadi *bullet points* atau *numbered lists* untuk komparasi, langkah-langkah, atau karakteristik.
*   **Gaya Bahasa:** Hindari kata-kata "slop" AI (seperti: krusial, penting untuk diingat, kesimpulannya, lanskap, dll). Gunakan bahasa akademik yang mengalir natural.

## 2. Pemetaan Target Gambar & Rumus per Bab

### Bagian I: Fondasi
*   **Bab 1: Evolusi Representasi Data**
    *   **Gambar (5):** (1) Diagram garis waktu ML klasik vs DL, (2) Hirarki Data -> Informasi -> Fitur, (3) Skema manual feature engineering, (4) Skema feature learning, (5) Diagram *No Free Lunch Theorem* dalam FE.
    *   **Rumus Utama:** Definisi formal fitur $X \rightarrow \hat{X}$, fungsi representasi $\phi(x)$.
*   **Bab 2: Anatomi dan Siklus Hidup Fitur**
    *   **Gambar (5):** (1) Tabel ke Matriks Fitur (Ilustrasi), (2) Siklus eksplorasi-ekstraksi-seleksi, (3) Diagram Feature Store, (4) Skema data leakage, (5) Train/Test split untuk FE.
    *   **Rumus Utama:** Perhitungan dasar *feature importance* (konseptual), rasio *missing values*.

### Bagian II: Pendekatan Berbasis Pengetahuan (Human-Designed)
*   **Bab 3: Pemrosesan Fitur Numerik Kontinu**
    *   **Gambar (6):** (1) Kurva distribusi normal vs skew, (2) Efek clipping/winsorization (sebelum/sesudah), (3) Plot log transform, (4) Box-cox transform Q-Q plot, (5) Binning histogram, (6) Skema scaling (MinMax vs Standard).
    *   **Rumus Utama:** Min-Max Scaler, Standard Scaler (Z-score), Log Transform, Box-Cox Transform, Robust Scaler.
*   **Bab 4: Fitur Kategorikal dan Ordinal**
    *   **Gambar (5):** (1) Matriks One-Hot Encoding, (2) Diagram ordinal mapping, (3) Skema Target Encoding (dengan K-Fold), (4) Dampak kardinalitas tinggi pada pohon, (5) Hash collision diagram.
    *   **Rumus Utama:** Target Encoding (smoothing formula $\lambda$), Hashing Trick.
*   **Bab 5: Fitur Interaksi, Polinomial, dan Sintetis**
    *   **Gambar (5):** (1) Geometri ruang fitur polinomial 2D ke 3D, (2) Pohon keputusan menangkap interaksi, (3) Skema PCA vs Interaksi manual, (4) Representasi rasio finansial, (5) Diagram SMOTE (sintesis data).
    *   **Rumus Utama:** Ekspansi Polinomial $(x_1 + x_2)^2$, SMOTE interpolation formula.
*   **Bab 6: Imputasi dan Penanganan Data Tidak Lengkap**
    *   **Gambar (5):** (1) Diagram MCAR, MAR, MNAR, (2) Efek imputasi mean pada varians, (3) Skema KNN imputation, (4) Skema Iterative/MICE imputation, (5) Mekanisme Missing Indicator.
    *   **Rumus Utama:** KNN Imputation (jarak), MICE (regresi berantai).
*   **Bab 7: Seleksi Fitur dan Pengurangan Dimensi**
    *   **Gambar (6):** (1) Curse of dimensionality (plot jarak), (2) Filter vs Wrapper vs Embedded, (3) Kurva ROC/AUC untuk seleksi, (4) Feature importance bar chart, (5) Forward vs Backward selection path, (6) Lasso shrinkage path.
    *   **Rumus Utama:** Pearson Correlation, Chi-Square, Mutual Information, L1 Regularization (Lasso) penalty term.

### Bagian III: Pendekatan Berbasis Algoritma & Model Terlatih
*   **Bab 8: Ekstraksi Fitur Geometris dan Topologis (PCA, t-SNE, UMAP)**
    *   **Gambar (6):** (1) Vektor Eigen pada PCA, (2) Skema reduksi linier vs non-linier, (3) Proyeksi t-SNE (kerumunan lokal), (4) Simplicial complex pada UMAP, (5) Trade-off perplexity, (6) Visualisasi 3D ke 2D.
    *   **Rumus Utama:** Dekomposisi Eigen (PCA), KL Divergence (t-SNE), Cross Entropy (UMAP).
*   **Bab 9: Feature Engineering Terotomatisasi (AutoFE)**
    *   **Gambar (5):** (1) Diagram arsitektur Deep Feature Synthesis (DFS), (2) Pohon relasi entitas, (3) Skema primitif agregasi/transformasi, (4) Evaluasi AutoFE vs Manual, (5) Pipeline AutoML (TPOT/Auto-sklearn).
    *   **Rumus Utama:** DFS depth calculation, Complexity penalty dalam seleksi AutoFE.
*   **Bab 10: Ekstraksi Fitur Runtun Waktu (Time Series)**
    *   **Gambar (6):** (1) Dekomposisi Tren/Musiman/Residu, (2) Jendela *rolling* dan *expanding*, (3) Fitur lag (korelasi autokorelasi), (4) Transformasi Fourier pada gelombang, (5) DTW (Dynamic Time Warping) alignment, (6) Skema ekstraksi tsfresh.
    *   **Rumus Utama:** Moving Average, Exponential Smoothing, Autocorrelation Function (ACF), Fast Fourier Transform (FFT).
*   **Bab 11: Ekstraksi Fitur Teks dan NLP Klasik**
    *   **Gambar (5):** (1) Diagram Bag-of-Words (BoW), (2) Pembobotan TF-IDF matriks term-dokumen, (3) N-gram overlap, (4) Stemming vs Lemmatization, (5) Batasan vektor sparse vs dense.
    *   **Rumus Utama:** Term Frequency (TF), Inverse Document Frequency (IDF), Jaccard Similarity, Cosine Similarity.
*   **Bab 12: Representasi Audio dan Sinyal**
    *   **Gambar (5):** (1) Waveform vs Spectrogram, (2) Jendela STFT (Short-Time Fourier Transform), (3) Skala Mel filterbank, (4) MFCC heatmap, (5) Ekstraksi Zero-Crossing Rate.
    *   **Rumus Utama:** STFT, Skala Mel (konversi frekuensi), Rumus dasar MFCC.

### Bagian IV: Transisi ke Representasi yang Dipelajari Mesin
*   **Bab 13: Graf dan Fitur Relasional**
    *   **Gambar (6):** (1) Jaringan node dan edge, (2) Matriks Adjacency, (3) Centrality (Degree, Betweenness), (4) Skema Random Walk (Node2Vec), (5) Pesan agregasi GNN, (6) Subgraf representasi.
    *   **Rumus Utama:** Degree Centrality, PageRank, Node2Vec objective function, GCN (Graph Convolutional Network) layer update.
*   **Bab 14: Vektor Padat (Embeddings) untuk Teks dan Gambar**
    *   **Gambar (6):** (1) Arsitektur Word2Vec (CBOW vs Skip-Gram), (2) Ruang vektor semantik (King - Man + Woman = Queen), (3) Convolutional filter pada CNN, (4) Flattening feature maps, (5) Diagram embedding BERT, (6) Contrastive Loss (CLIP).
    *   **Rumus Utama:** Skip-gram Softmax, Attention Mechanism, Triplet/Contrastive Loss.
*   **Bab 15: Ekstraksi dari Model Terlatih (Pre-trained Models/Transfer Learning)**
    *   **Gambar (5):** (1) Skema Transfer Learning (membekukan layer), (2) ResNet bottleneck, (3) Ekstraksi CLS token dari Transformer, (4) Fine-tuning vs Feature Extraction, (5) Arsitektur HuggingFace pipeline.
    *   **Rumus Utama:** Cross-Entropy dengan pre-trained weights, Knowledge Distillation loss (opsional).

### Bagian V: Aspek Lanjutan
*   **Bab 16: Feature Engineering Terbantu LLM (LLM-Assisted FE)**
    *   **Gambar (5):** (1) Pipeline CAAFE, (2) Prompting untuk menghasilkan nama fitur baru, (3) Verifikasi logika kode oleh agen, (4) Penjelasan SHAP dari LLM, (5) Data Tabular ke Prompt Teks.
    *   **Rumus Utama:** Bayesian optimization acquisition function (dalam konteks iterasi agen).
*   **Bab 17: Rekayasa Fitur dalam Produksi**
    *   **Gambar (6):** (1) Skema Training-Serving Skew, (2) Arsitektur Feature Store (Feast/Hopsworks), (3) Batch vs Streaming features, (4) Monitoring drift fitur (Data Drift diagram), (5) CI/CD untuk fitur, (6) Arsitektur hybrid.
    *   **Rumus Utama:** PSI (Population Stability Index), Wasserstein Distance.
