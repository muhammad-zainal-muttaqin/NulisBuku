# Opsi Dataset Mini-Project per Bab

> Buku: **Rekayasa Fitur Modern** (Fatma Indriani) — 17 bab.
> Disusun 2026-07-03. Semua dataset **nyata** dan dapat diunduh gratis (HuggingFace / Kaggle / UCI / scikit-learn).
> Tiap bab diberi 2–3 opsi supaya bisa dipilah.
>
> **Keterangan sumber:**
> - `sklearn`/`seaborn` = built-in, langsung lewat fungsi (tanpa unduh manual, tanpa login).
> - `HF` = HuggingFace Datasets (`load_dataset("...")`).
> - `Kaggle` = perlu akun Kaggle.
> - `UCI` = UCI Machine Learning Repository.
> - 🇮🇩 = dataset berbahasa/berkonteks Indonesia.
> - Semua dataset di sini berbeda dari contoh yang sudah dipakai di dalam buku (iris, Ames, CIFAR-10).
> - Link Kaggle bertipe *competition* (`/c/...`) mengharuskan klik **"Join Competition"** & setujui rules dulu sebelum tab **Data** bisa diunduh. Link bertipe `/datasets/...` bisa langsung diunduh.

---

## Bab 1 — Data, Atribut, Fitur, dan Representasi

| Dataset | Sumber | Link | Penjelasan singkat |
|---|---|---|---|
| Palmer Penguins | seaborn | https://allisonhorst.github.io/palmerpenguins/ | 344 penguin, campuran atribut numerik + kategori + missing; ideal membedakan jenis atribut. |
| Titanic | seaborn / Kaggle | https://www.kaggle.com/c/titanic | Data penumpang Titanic; klasik untuk membedakan data mentah vs fitur siap-model. |
| Online Retail II | UCI | https://archive.ics.uci.edu/dataset/502/online+retail+ii | ~1 juta transaksi ritel online (2009–2011); contoh raw data yang belum jadi fitur. |

## Bab 2 — Fit & Transform (Pipeline)

| Dataset | Sumber | Link | Penjelasan singkat |
|---|---|---|---|
| Adult / Census Income | UCI | https://archive.ics.uci.edu/dataset/2/adult | Prediksi pendapatan >50K dari data sensus; train-test jelas, wajib fit hanya di train. |
| Bank Marketing | UCI | https://archive.ics.uci.edu/dataset/222/bank+marketing | Kampanye telemarketing bank Portugal; campuran numerik+kategori untuk latih ColumnTransformer. |
| Wine Quality | UCI | https://archive.ics.uci.edu/dataset/109/wine | Uji fisikokimia anggur → skor kualitas; kecil & bersih, fokus ke mekanik pipeline. |

## Bab 3 — Skala & Distribusi (Fitur Numerik)

| Dataset | Sumber | Link | Penjelasan singkat |
|---|---|---|---|
| California Housing | sklearn | https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_california_housing.html | Harga rumah California; fitur berskala jauh beda + skewed (income, populasi). |
| Bike Sharing | UCI | https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset | Jumlah sewa sepeda per jam/hari; banyak numerik rentang beda, uji StandardScaler vs RobustScaler. |
| Concrete Compressive Strength | UCI | https://archive.ics.uci.edu/dataset/165/concrete+compressive+strength | 1030 sampel beton, 8 fitur bahan (semen, air, agregat, umur) dengan skala sangat berbeda; ideal StandardScaler & log. |

## Bab 4 — Encoding Kategorikal

| Dataset | Sumber | Link | Penjelasan singkat |
|---|---|---|---|
| Mushroom | UCI | https://archive.ics.uci.edu/dataset/73/mushroom | Klasifikasi jamur beracun/aman; 100% fitur kategorikal, ideal one-hot vs ordinal. |
| Telco Customer Churn | Kaggle | https://www.kaggle.com/datasets/blastchar/telco-customer-churn | Pelanggan telekomunikasi + label churn; kardinalitas rendah–sedang. |
| Cat-in-the-Dat | Kaggle | https://www.kaggle.com/c/cat-in-the-dat | Dataset khusus latihan encoding: nominal, ordinal, cyclical, dan high-cardinality. |

## Bab 5 — Missing Values & Outlier

| Dataset | Sumber | Link | Penjelasan singkat |
|---|---|---|---|
| Titanic | Kaggle | https://www.kaggle.com/c/titanic | Kolom Age/Cabin banyak kosong; kasus MCAR/MAR yang nyata. |
| Melbourne Housing | Kaggle | https://www.kaggle.com/datasets/dansbecker/melbourne-housing-snapshot | Harga rumah Melbourne; banyak kolom kosong + harga outlier. |
| Horse Colic | UCI | https://archive.ics.uci.edu/dataset/47/horse+colic | Data medis kuda dengan ~30% nilai hilang; klasik untuk strategi imputasi. |

## Bab 6 — Fitur Turunan (Rasio, Selisih, Interaksi)

| Dataset | Sumber | Link | Penjelasan singkat |
|---|---|---|---|
| NYC Taxi Trip Duration | Kaggle | https://www.kaggle.com/c/nyc-taxi-trip-duration | Perjalanan taksi + koordinat & timestamp; turunkan jarak, kecepatan, fitur waktu. |
| Home Credit Default Risk | Kaggle | https://www.kaggle.com/c/home-credit-default-risk | Data kredit; kaya rasio finansial (utang/pendapatan, dsb). |
| Credit Card Customers (BankChurners) | Kaggle | https://www.kaggle.com/datasets/sakshigoyal7/credit-card-customers | 10k nasabah kartu kredit; turunkan rasio utilisasi (saldo/limit), rata-rata transaksi, dsb. |

## Bab 7 — Feature Selection

| Dataset | Sumber | Link | Penjelasan singkat |
|---|---|---|---|
| Madelon | UCI | https://archive.ics.uci.edu/dataset/171/madelon | Dirancang khusus untuk seleksi fitur; banyak fitur noise/tidak relevan. |
| Breast Cancer Wisconsin | sklearn | https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_breast_cancer.html | 30 fitur diagnosis kanker yang saling berkorelasi; latih buang redundansi. |
| Santander Customer Satisfaction | Kaggle | https://www.kaggle.com/c/santander-customer-satisfaction | 370 fitur anonim, banyak konstan/duplikat; kasus reduksi fitur skala besar. |

## Bab 8 — Reduksi Dimensi (PCA / t-SNE / UMAP)

| Dataset | Sumber | Link | Penjelasan singkat |
|---|---|---|---|
| Digits | sklearn | https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html | Citra angka 8×8 (64-dim); cepat untuk PCA + visualisasi 2D. |
| Fashion-MNIST | HF | https://huggingface.co/datasets/zalando-datasets/fashion_mnist | 70k citra pakaian 28×28 (784-dim); bagus untuk t-SNE/UMAP. |
| Human Activity Recognition (HAR) | UCI | https://archive.ics.uci.edu/dataset/240/human+activity+recognition+using+smartphones | 561 fitur sensor smartphone; kompresi dimensi yang nyata. |

## Bab 9 — Kualitas Fitur di Produksi (Drift, Availability)

| Dataset | Sumber | Link | Penjelasan singkat |
|---|---|---|---|
| Electricity (elec2) | OpenML | https://www.openml.org/d/151 | Permintaan listrik NSW; dataset standar untuk *concept drift* temporal. |
| Give Me Some Credit | Kaggle | https://www.kaggle.com/c/GiveMeSomeCredit | Skor kredit; bahas availability fitur saat inference (scoring real-time). |
| IEEE-CIS Fraud Detection | Kaggle | https://www.kaggle.com/c/ieee-fraud-detection | Transaksi fraud; latensi & stabilitas fitur di produksi. |

## Bab 10 — Sampel Temporal (Windowing Time Series)

| Dataset | Sumber | Link | Penjelasan singkat |
|---|---|---|---|
| Jena Climate 2009–2016 | Keras/TF | https://keras.io/examples/timeseries/timeseries_weather_forecasting/ | Cuaca per 10 menit; standar untuk demo lookback/horizon/stride. |
| Household Power Consumption | UCI | https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption | Konsumsi listrik rumah per menit selama ~4 tahun; deret sangat panjang. |
| Air Quality | UCI | https://archive.ics.uci.edu/dataset/360/air+quality | Sensor kualitas udara per jam; multivariat, latih penyelarasan target masa depan. |

## Bab 11 — Representasi Teks Klasik (BoW / TF-IDF)

| Dataset | Sumber | Link | Penjelasan singkat |
|---|---|---|---|
| IMDB Reviews | HF | https://huggingface.co/datasets/stanfordnlp/imdb | 50k ulasan film (sentimen biner); TF-IDF + logistic regression. |
| SMS Spam Collection | HF / UCI | https://huggingface.co/datasets/ucirvine/sms_spam | 5.5k SMS spam vs ham; kecil & cepat untuk BoW. |
| 🇮🇩 IndoNLU SmSA | HF | https://huggingface.co/datasets/indonlp/indonlu | Sentimen Bahasa Indonesia (positif/negatif/netral); pakai config `smsa`. |
| 🇮🇩 PRDECT-ID | Kaggle | https://www.kaggle.com/datasets/jocelyndumlao/prdect-id-indonesian-emotion-classification | 5.4k ulasan produk Tokopedia beranotasi emosi + sentimen. |

## Bab 12 — Citra (Normalisasi & Augmentasi)

| Dataset | Sumber | Link | Penjelasan singkat |
|---|---|---|---|
| Beans | HF | https://huggingface.co/datasets/AI-Lab-Makerere/beans | Citra daun kacang (3 kelas); kecil, cepat untuk demo augmentasi. |
| Food-101 | HF | https://huggingface.co/datasets/ethz/food101 | 101k foto makanan (101 kelas); augmentasi warna/crop terlihat jelas. |
| Cats vs Dogs | HF | https://huggingface.co/datasets/microsoft/cats_vs_dogs | ~23k foto kucing/anjing beresolusi beragam; realistis untuk normalisasi & augmentasi (resize, crop, flip). |

## Bab 13 — Data Spasial (Koordinat / Geo)

| Dataset | Sumber | Link | Penjelasan singkat |
|---|---|---|---|
| NYC Taxi | Kaggle | https://www.kaggle.com/c/nyc-taxi-trip-duration | Koordinat lat/long pickup–dropoff; hitung jarak Haversine. |
| 🇮🇩 Daftar Harga Rumah Jabodetabek | Kaggle | https://www.kaggle.com/datasets/nafisbarizki/daftar-harga-rumah-jabodetabek | 3.554 rumah Jabodetabek dengan kolom Lat/Long + harga; hitung fitur kedekatan/jarak antar-lokasi. |
| California Housing | sklearn | https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_california_housing.html | Ada lat/long; cluster spasial harga rumah. |

## Bab 14 — Data Multimodal

| Dataset | Sumber | Link | Penjelasan singkat |
|---|---|---|---|
| Flickr30k | HF | https://huggingface.co/datasets/nlphuji/flickr30k | 31k citra + caption teks; latih penyelarasan gambar–teks. |
| Amazon Reviews 2023 | HF | https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023 | Ulasan teks + metadata tabular (+gambar produk); fusi modalitas. |
| Hateful Memes | Kaggle | https://www.kaggle.com/datasets/parthplc/facebook-hateful-meme-dataset | Meme (citra + teks) untuk klasifikasi gabungan; mirror unduh langsung dari challenge Meta AI. |

## Bab 15 — Embedding / Transfer Learning (Frozen → Fine-Tune)

| Dataset | Sumber | Link | Penjelasan singkat |
|---|---|---|---|
| AG News | HF | https://huggingface.co/datasets/fancyzhx/ag_news | Klasifikasi 4 topik berita; teks + DistilBERT, bandingkan frozen vs fine-tune. |
| Beans | HF | https://huggingface.co/datasets/AI-Lab-Makerere/beans | Citra + ViT/ResNet pretrained sebagai frozen extractor. |
| 🇮🇩 IndoNLU SmSA + IndoBERT | HF | https://huggingface.co/datasets/indonlp/indonlu | Spektrum adaptasi Bahasa Indonesia (pakai model `indobenchmark/indobert-base-p1`). |

## Bab 16 — Automated Feature Engineering (DFS / FeatureTools)

| Dataset | Sumber | Link | Penjelasan singkat |
|---|---|---|---|
| Olist Brazilian E-commerce | Kaggle | https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce | 9 tabel relasional (order, produk, review, dll); ideal DFS multi-tabel. |
| Instacart Market Basket (mirror) | Kaggle | https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis | 6 tabel (orders, products, aisles, departments, order_products); relasi order → produk untuk agregasi bertingkat. |
| FeatureTools demo (`retail`) | FeatureTools | https://featuretools.alteryx.com/ | EntitySet bawaan; langsung jalan tanpa unduh manual. |

## Bab 17 — Rancangan Pipeline End-to-End

| Dataset | Sumber | Link | Penjelasan singkat |
|---|---|---|---|
| Telco Customer Churn | Kaggle | https://www.kaggle.com/datasets/blastchar/telco-customer-churn | Lengkap dari definisi target → split → pipeline final. |
| Home Credit Default Risk | Kaggle | https://www.kaggle.com/c/home-credit-default-risk | Realistis; ada risiko leakage & horizon waktu untuk latih split. |
| Rossmann Store Sales | Kaggle | https://www.kaggle.com/c/rossmann-store-sales | Gabungan temporal + tabular; wajib split berbasis waktu. |

---

## Ringkasan cara akses (untuk memilah cepat)

- **Tanpa login, paling gampang:** `sklearn`/`seaborn` (California Housing, Digits, Breast Cancer, Penguins, Titanic) dan `HF` (IMDB, AG News, Beans, Fashion-MNIST, IndoNLU, Food-101).
- **Perlu akun Kaggle:** Titanic, Telco, Home Credit, NYC Taxi, Olist, Rossmann, Cat-in-the-Dat, Santander, IEEE Fraud, dll.
- **UCI:** unduh langsung dari halaman dataset atau lewat paket `ucimlrepo`.
- **Opsi Indonesia 🇮🇩:** Bab 11 (IndoNLU, PRDECT-ID), Bab 13 (Inside Airbnb Jakarta), Bab 15 (IndoNLU + IndoBERT).
