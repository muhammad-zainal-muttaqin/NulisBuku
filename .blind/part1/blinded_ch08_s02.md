# Blind Writer Evaluation - ch08_s02: PCA and SVD / truncated SVD 🔢  *(technical subsection)*

Score each sample **1-5** on three dimensions (see the rubric):
**D1 Naturalness & correctness . D2 Register & accessibility . D3 Technical & terminological fidelity.**
Please do not try to guess which model wrote which sample.

## Sample 1

## 8.2 PCA dan SVD: Dekomposisi Linier

*Principal Component Analysis* (*PCA*) menemukan arah ortogonal, yang disebut *principal component*, yang memaksimalkan varians data. Jika kita memiliki matriks data terpusat $X \in \mathbb{R}^{n \times d}$, kita dapat menghitung matriks kovarians $C = \tfrac{1}{n-1} X^\top X$. Komponen dan variansnya diperoleh melalui dekomposisi *eigenvalue*: $C\mathbf{w}_i = \lambda_i \mathbf{w}_i$, di mana $\mathbf{w}_i$ adalah *eigenvector* dan $\lambda_i$ merepresentasikan varians.

Proyeksi data ke $k$ komponen teratas menghasilkan representasi berdimensi lebih rendah, $Z = X W_k$, dengan $W_k = [\mathbf{w}_1, \dots, \mathbf{w}_k]$. Fraksi varians total yang ditangkap oleh suatu komponen dihitung melalui rasio $\dfrac{\lambda_i}{\sum_j \lambda_j}$. Untuk memilih $k$, kita mengamati varians kumulatif. Gambar 8.1 memperlihatkan plot *scree* yang memetakan varians kumulatif terhadap jumlah komponen; titik siku pada plot ini sering menjadi panduan untuk memilih $k$ yang optimal.

[GAMBAR 8.1]
Judul: Plot varians kumulatif dan titik siku untuk pemilihan komponen
Tipe: plot data
Tampilkan: Sumbu x menampilkan jumlah komponen, sumbu y menampilkan proporsi varians kumulatif, dengan titik siku (elbow) yang jelas.
Sumber data: notebook Bab 8

Pendekatan ekuivalen untuk PCA adalah *Singular Value Decomposition* (*SVD*) pada matriks data terpusat, $X = U\Sigma V^\top$. Pendekatan *truncated SVD* melakukan faktorisasi matriks dan hanya mempertahankan $k$ nilai singular teratas sebagai aproksimasi peringkat rendah, $X_k = U_k \Sigma_k V_k^\top$. Karena tidak memerlukan perhitungan matriks kovarians, *truncated SVD* sangat efisien untuk data *sparse* dan menjadi standar untuk representasi teks melalui *Latent Semantic Analysis* (*LSA*). Di scikit-learn, kita menggunakan `PCA` untuk data padat dan `TruncatedSVD` untuk data *sparse*, keduanya dikendalikan oleh parameter `n_components`.

Penggunaan $k$ bergantung pada tujuan. Untuk visualisasi, kita mereduksi data menjadi dua komponen. Untuk pemodelan, kita biasanya mempertahankan komponen hingga mencapai sekitar 95% varians kumulatif (dapat dicek melalui atribut `explained_variance_ratio_`). Namun, ada beberapa catatan penting. Komponen PCA adalah kombinasi linier dari fitur asli sehingga sulit diinterpretasikan. PCA juga sangat sensitif terhadap skala, sehingga data perlu di-*standardize* terlebih dahulu menggunakan `StandardScaler`. Terakhir, PCA hanya menangkap struktur linier.

Dari spektrum rekayasa fitur, representasi PCA condong ke arah *dipelajari mesin* karena diekstraksi secara algoritmik dari data. Namun, karena dihitung dari data kita sendiri dan bukan ditransfer dari model eksternal, teknik ini tetap berada di ranah Bab 8, bukan Bab 15. Dalam disiplin *pipeline*, pastikan kita hanya melakukan *fit* pada data latih, lalu mentransformasi data latih dan data uji agar tidak terjadi kebocoran data.

---

## Sample 2

### 8.2 PCA dan *Truncated SVD*

*Principal Component Analysis* (*PCA*) adalah metode pereduksian dimensi klasik yang bekerja dengan mencari arah ortogonal bervarians maksimum di dalam data, yang disebut *principal component*. Karena PCA sangat sensitif terhadap perbedaan skala antarfitur, kita harus selalu melakukan *standardize* pada data terlebih dahulu, misalnya menggunakan `StandardScaler`.

Secara matematis, kita mulai dengan matriks data yang sudah dipusatkan (rata-rata nol), $X \in \mathbb{R}^{n \times d}$. PCA menghitung matriks kovarians $C = \tfrac{1}{n-1} X^\top X$. Arah varians maksimum ditemukan melalui dekomposisi *eigenvalue* dari matriks tersebut: $C\mathbf{w}_i = \lambda_i \mathbf{w}_i$, di mana $\mathbf{w}_i$ adalah *eigenvector* dan $\lambda_i$ adalah *eigenvalue*. Untuk mereduksi dimensi data menjadi $k$, kita memproyeksikan data awal ke dalam $k$ komponen teratas: $Z = X W_k$, dengan $W_k = [\mathbf{w}_1, \dots, \mathbf{w}_k]$. Karena letak komponen baru ini merupakan kombinasi linear dari fitur-fitur asli, maknanya sering kali menjadi kurang intuitif untuk diinterpretasikan secara langsung.

Selain melalui dekomposisi matriks kovarians, ada jalur perhitungan lain yang ekuivalen dan lebih stabil secara numerik, yaitu *Singular Value Decomposition* (*SVD*). SVD memfaktorkan matriks data langsung menjadi $X = U\Sigma V^\top$. Varian yang paling sering dipakai dalam rekayasa fitur adalah *truncated SVD*, yaitu faktorisasi tingkat rendah (low-rank) yang hanya mempertahankan $k$ nilai singular teratas: $X_k = U_k \Sigma_k V_k^\top$. Berbeda dengan PCA standar, *truncated SVD* tidak memerlukan tahap pemusatan data dan perhitungan matriks kovarians. Hal ini membuatnya mampu menangani data *sparse* secara efisien, sehingga menjadi standar de facto untuk pemrosesan teks seperti *LSA* (menggunakan kelas `TruncatedSVD`).

Bagaimana kita memilih nilai $k$ (parameter `n_components` pada antarmuka `PCA`)? Keputusan ini didasarkan pada proporsi varians yang ditangkap oleh setiap komponen, yang dirumuskan dengan $\dfrac{\lambda_i}{\sum_j \lambda_j}$ dan dapat diakses melalui atribut `explained_variance_ratio_`.

[GAMBAR 8.1]
Judul: Kurva *scree* untuk memilih jumlah komponen.
Tipe: plot data
Tampilkan: Sumbu x mewakili jumlah komponen, sumbu y mewakili proporsi varians kumulatif, dengan titik siku (elbow) yang jelas.
Sumber data: notebook Bab 8.

Gambar 8.1 memperlihatkan plot *scree*, sebuah alat bantu visual untuk melihat kumulasi varians. Sebagai contoh penggunaan, kita mungkin memproyeksikan data dimensi tinggi ke dalam 2 komponen saja jika tujuannya adalah visualisasi dua dimensi. Namun, jika tujuannya adalah kompresi untuk pemodelan prediktif, kita biasanya mencari titik siku pada kurva dan mempertahankan jumlah komponen yang cukup untuk menangkap sekitar 95% varians kumulatif.

Ada beberapa catatan penting saat menggunakan metode ini. Pertama, PCA hanya mampu menangkap struktur linear; pola data non-linear akan membutuhkan metode lain. Kedua, dalam spektrum rekayasa fitur, representasi PCA merupakan representasi yang *dipelajari mesin* karena diturunkan secara algoritmik dari data. Akan tetapi, representasi ini dihitung secara spesifik dari data kita sendiri, bukan ditransfer dari luar seperti *embedding* pralatih yang akan kita bahas pada Bab 15. Terakhir, disiplin alur kerja (pipeline) tetap berlaku mutlak: lakukan *fit* pada objek PCA hanya menggunakan data latih, kemudian gunakan objek tersebut untuk melakukan *transform* pada data latih dan data uji demi mencegah kebocoran informasi.

---

## Sample 3

### 8.2 *PCA* dan *SVD* / *truncated SVD*

Dalam *PCA*, reduksi dimensi dilakukan dengan mencari sumbu baru, bukan memilih sebagian fitur lama. Setiap *principal component* adalah arah ortogonal yang menangkap varians sebesar mungkin. Proyeksi ke komponen teratas memberi representasi lebih ringkas. Untuk visualisasi, dataset berdimensi tinggi dapat dipadatkan menjadi 2 komponen; untuk pemodelan, kita dapat menyimpan komponen secukupnya, misalnya hingga sekitar 95% varians kumulatif.

Untuk matriks data terpusat $X \in \mathbb{R}^{n \times d}$, kovariansnya adalah $C = \tfrac{1}{n-1} X^\top X$. Komponen dan variansnya diperoleh dari $C\mathbf{w}_i = \lambda_i \mathbf{w}_i$. Vektor $\mathbf{w}_i$ adalah *eigenvector* yang menjadi komponen, sedangkan $\lambda_i$ adalah *eigenvalue* yang menyatakan besar varians pada arah tersebut. Komponen diurutkan dari $\lambda_i$ terbesar ke terkecil. Karena itu, *variance explained* adalah fraksi varians total yang ditangkap sebuah komponen, yaitu $\dfrac{\lambda_i}{\sum_j \lambda_j}$. Jika $W_k = [\mathbf{w}_1, \dots, \mathbf{w}_k]$, proyeksi ke $k$ dimensi ditulis $Z = X W_k$.

Jalur lain yang setara adalah *SVD* pada data terpusat: $X = U\Sigma V^\top$. *Truncated SVD* menyimpan hanya $k$ nilai singular terbesar, sehingga menghasilkan faktorisasi *low-rank* $X_k = U_k \Sigma_k V_k^\top$. Karena tidak perlu membentuk kovarians, teknik ini cocok untuk data *sparse*, terutama teks, dan sering muncul sebagai *LSA*. Di `sklearn.decomposition`, gunakan `PCA` dengan `n_components` serta atribut `explained_variance_ratio_`; untuk teks atau data *sparse*, gunakan `TruncatedSVD` dengan `n_components`.

Pemilihan $k$ biasanya dibantu oleh kurva varians kumulatif atau plot *scree*. Titik *elbow* menandai saat penambahan komponen mulai memberi keuntungan kecil.

[GAMBAR 8.1]
Judul: Varians kumulatif untuk memilih jumlah komponen
Tipe: plot data
Tampilkan: x = jumlah komponen, y = proporsi varians kumulatif, dengan titik siku (elbow)
Sumber data: notebook Bab 8

Gambar 8.1 dibaca sebagai trade-off: semakin ke kanan, informasi yang tersimpan makin besar, tetapi representasi juga makin kurang ringkas.

Ada beberapa batasan. Komponen *PCA* adalah kombinasi linear fitur asal, sehingga interpretasinya tidak selalu mudah. *PCA* juga sensitif terhadap skala; jika skala fitur berbeda, lakukan *standardize* lebih dulu dengan `StandardScaler`. Selain itu, *PCA* hanya menangkap struktur linear; struktur nonlinear menjadi alasan kita membahas pendekatan lain pada bagian berikutnya.

**Posisi spektrum:** dibandingkan representasi yang dirancang manusia, *PCA* lebih condong ke representasi yang dipelajari mesin karena dihitung dari data oleh algoritma. Namun, datanya tetap data kita sendiri, bukan transfer dari luar seperti *pretrained embedding*. Inilah batas penting Bab 8 dan Bab 15.

**Disiplin *pipeline*:** lakukan *fit* `StandardScaler` dan `PCA` hanya pada data latih, lalu *transform* data latih dan data uji dengan objek yang sama.

---

## Sample 4

8.2 PCA dan SVD Terpampat

*PCA* (Principal Component Analysis) mencari arah orthogonal yang menangkap varians terbesar di dalam data. Arah tersebut disebut *principal component*. Dengan memproyeksikan data ke *k* komponen teratas, kita memperoleh representasi berdimensi lebih rendah yang tetap mempertahankan sebanyak mungkin informasi.

Mekanismenya dimulai dengan memusatkan data sehingga rata-rata setiap fitur menjadi nol. Dari matriks data yang sudah dipusatkan \(X \in \mathbb{R}^{n \times d}\), kita hitung matriks kovarians \(C = \tfrac{1}{n-1} X^\top X\). Komponen utama dan proporsi varians yang dijelaskannya diperoleh melalui eigendekomposisi \(C\mathbf{w}_i = \lambda_i \mathbf{w}_i\). Komponen diurutkan menurut nilai eigenvalue \(\lambda_i\) yang semakin menurun.

Rute yang setara adalah melakukan *SVD* langsung pada matriks \(X\) yang sudah dipusatkan: \(X = U\Sigma V^\top\). *Truncated SVD* hanya menyimpan *k* nilai singular terbesar sehingga menghasilkan aproksimasi berperingkat rendah \(X_k = U_k \Sigma_k V_k^\top\). Karena tidak perlu membentuk matriks kovarians, *truncated SVD* lebih efisien untuk data *sparse* dan sering dipakai pada teks (*LSA*).

Proyeksi data ke ruang komponen terpilih dilakukan dengan \(Z = X W_k\), di mana \(W_k = [\mathbf{w}_1, \dots, \mathbf{w}_k]\). Proporsi varians yang dijelaskan oleh komponen ke-\(i\) adalah \(\dfrac{\lambda_i}{\sum_j \lambda_j}\).

Untuk menentukan *k*, praktisi biasanya melihat plot *scree* atau kurva varians kumulatif. Titik siku (elbow) menandai jumlah komponen yang sudah cukup menangkap sebagian besar varians.

Gambar 8.1 memperlihatkan contoh kurva tersebut. Sumbu horizontal adalah jumlah komponen, sumbu vertikal adalah proporsi varians kumulatif. Pembaca dapat membaca titik di mana kenaikan sudah melandai untuk memilih *k*.

Dua kasus penggunaan yang berbeda sering muncul. Untuk visualisasi, kita biasanya memilih *k*=2 atau 3 agar data dapat digambarkan. Untuk keperluan pemodelan selanjutnya, kita pilih *k* yang menjelaskan sekitar 95 % varians total sehingga informasi penting tetap terjaga tanpa membuang terlalu banyak dimensi.

Beberapa hal perlu diperhatikan. Setiap komponen merupakan kombinasi linear dari fitur asli, sehingga interpretasinya tidak langsung. *PCA* sangat sensitif terhadap skala; oleh karena itu fitur sebaiknya *standardize* terlebih dahulu dengan `StandardScaler` sebelum *PCA* dijalankan. Karena bersifat linear, *PCA* tidak menangkap struktur nonlinear; metode manifold atau *autoencoder* akan dibahas pada subbab berikutnya.

Dalam alur kerja, objek `PCA` atau `TruncatedSVD` dari *scikit-learn* hanya dipasang pada bagian pelatihan, kemudian transformasi yang sama diterapkan ke data validasi dan uji. Hal ini mencegah kebocoran informasi.

Representasi yang dihasilkan *PCA* diperoleh melalui algoritma yang bekerja pada data kita sendiri. Ia berada di sisi *dipelajari mesin* dalam spektrum bab ini, namun tetap berbeda dari representasi yang ditransfer dari model pralatih di bab lain.

---

## Sample 5

## 8.2 PCA dan SVD (*Truncated SVD*)

Kita telah melihat di subbab sebelumnya bahwa reduksi dimensi bisa dilakukan untuk dua keperluan yang berbeda: kompresi data kita sendiri atau visualisasi. Di subbab ini kita membahas dua metode linear yang paling mendasar, *Principal Component Analysis* (PCA) dan dekomposisi nilai singular terpotong (*truncated SVD*).

PCA mencari arah-arah ortogonal, yang disebut *principal component*, sedemikian rupa sehingga data memiliki varians paling besar ketika diproyeksikan ke arah tersebut. Arah pertama menangkap varians terbesar, arah kedua menangkap varians terbesar yang tersisa dan tegak lurus terhadap arah pertama, dan seterusnya. Dengan mengambil hanya *k* komponen pertama, kita memperoleh representasi data dalam ruang berdimensi lebih rendah yang mempertahankan sebanyak mungkin informasi varians.

Mekanisme PCA berangkat dari data yang telah dipusatkan, $X \in \mathbb{R}^{n \times d}$. Matriks kovarians dihitung sebagai $C = \frac{1}{n-1} X^\top X$. Vektor eigen $\mathbf{w}_i$ dan nilai eigen $\lambda_i$ dari $C$ memenuhi $C\mathbf{w}_i = \lambda_i \mathbf{w}_i$. Komponen utama adalah vektor eigen dengan nilai eigen terbesar; $\lambda_i$ mengukur varians yang ditangkap oleh komponen ke-$i$. Proyeksi data ke ruang *k* komponen dilakukan dengan $Z = X W_k$ di mana $W_k = [\mathbf{w}_1, \dots, \mathbf{w}_k]$.

Pendekatan yang setara dan lebih stabil secara numerik adalah *SVD* pada matriks data terpusat: $X = U\Sigma V^\top$. Matriks $V$ berisi vektor eigen yang sama, dan kuadrat nilai singular di $\Sigma$ sebanding dengan nilai eigen. *Truncated SVD* cukup mempertahankan $k$ nilai singular terbesar, menghasilkan aproksimasi peringkat rendah $X_k = U_k \Sigma_k V_k^\top$. Kelebihan rute ini adalah tidak perlu menghitung kovarians secara eksplisit, sehingga cocok untuk data yang sangat *sparse*, seperti matriks dokumen-kata pada *Latent Semantic Analysis* (LSA).

Memilih $k$ yang tepat umumnya dilakukan dengan melihat proporsi varians kumulatif yang dijelaskan, $\frac{\sum_{i=1}^k \lambda_i}{\sum_{j} \lambda_j}$. Plot *scree* (Gambar 8.1) memperlihatkan proporsi ini terhadap jumlah komponen; titik siku (*elbow*) menjadi petunjuk di mana penambahan komponen berikutnya hanya memberi tambahan varians yang kecil.

[GAMBAR 8.1]  
Judul: Proporsi varians kumulatif terhadap jumlah komponen PCA  
Tipe: plot data  
Tampilkan: sumbu x = jumlah komponen, sumbu y = proporsi varians kumulatif; titik siku (elbow) ditandai.  
Sumber data: notebook Bab 8

Dalam praktik, dua skenario penggunaan yang umum: untuk visualisasi, kita sering mereduksi data menjadi dua komponen agar dapat digambar di bidang; untuk pemodelan, kita dapat mempertahankan cukup komponen hingga varians kumulatif mencapai sekitar 95%. Kedua pilihan ini mewakili trade-off antara kemudahan interpretasi visual dan kesetiaan informasi.

Meskipun populer, PCA memiliki keterbatasan. Komponen yang dihasilkan adalah kombinasi linear dari fitur-fitur asli, sehingga sulit ditafsirkan secara intuitif. PCA juga sangat sensitif terhadap skala; fitur dengan rentang lebar akan mendominasi varians. Karena itu, sangat penting untuk melakukan *standardize* (misalnya menggunakan `StandardScaler`) sebelum menerapkan PCA pada data yang fiturnya berbeda satuan. Selain itu, PCA hanya menangkap struktur linear; pola non-linear perlu ditangani dengan metode manifold atau *autoencoder* yang akan dibahas di subbab-subbab berikutnya.

Dari sisi spektrum representasi, PCA berada di posisi yang unik: arah-arah komponen dihitung sepenuhnya oleh algoritma dari data yang kita miliki, sehingga prosesnya condong ke sisi *dipelajari mesin*. Namun, representasi yang dihasilkan bersifat spesifik pada data latih itu sendiri, bukan representasi yang sudah di-*pre-train* dari korpus luar — inilah perbedaan mendasar antara Bab 8 (reduksi intrinsik) dan Bab 15 (representasi yang ditransfer). Karena alasan ini, disiplin pipeline tetap berlaku: PCA hanya di-fit pada data latih, lalu data validasi dan uji ditransformasi dengan komponen yang sama, menghindari kebocoran informasi antar himpunan data.

---

## Sample 6

## 8.2 PCA dan SVD: Menemukan Arah Varians Terbesar

*PCA* (*Principal Component Analysis*) berangkat dari pertanyaan sederhana: ke arah mana data paling "menyebar"? Arah-arah itulah yang paling informatif, dan memproyeksikan data ke sana berarti kita mempertahankan informasi terbanyak dengan dimensi sesedikit mungkin.

Prosedurnya dimulai dengan memusatkan data — mengurangkan rata-rata tiap fitur sehingga distribusi berpusat di origin. Misalkan matriks data yang telah dimusatkan adalah $X \in \mathbb{R}^{n \times d}$. Kovarians antar-fitur terangkum dalam $C = \tfrac{1}{n-1} X^\top X$. Dekomposisi eigen matriks ini, $C\mathbf{w}_i = \lambda_i \mathbf{w}_i$, menghasilkan *eigenvector* $\mathbf{w}_i$ sebagai *principal component* — arah ortogonal dengan varians maksimum — dan *eigenvalue* $\lambda_i$ yang mengukur seberapa besar varians tercakup di arah tersebut. Rasio $\lambda_i / \sum_j \lambda_j$ adalah *variance explained* oleh komponen ke-$i$.

Jalur komputasi yang setara, dan sering lebih stabil secara numerik, adalah *SVD*: $X = U\Sigma V^\top$. Kolom-kolom $V$ adalah *eigenvector* kovarians, dan nilai-nilai singular di diagonal $\Sigma$ berhubungan langsung dengan *eigenvalue*. Proyeksi ke $k$ komponen teratas ditulis $Z = X W_k$, di mana $W_k = [\mathbf{w}_1, \dots, \mathbf{w}_k]$.

*Truncated SVD* mengambil ide ini lebih jauh: alih-alih menghitung dekomposisi penuh, kita hanya simpan $k$ nilai singular terbesar sehingga $X_k = U_k \Sigma_k V_k^\top$ menjadi aproksimasi rank rendah. Keunggulannya adalah kemampuannya bekerja langsung pada data *sparse* tanpa perlu memusatkan matriks, menjadikannya pilihan utama untuk teks. Dalam konteks teks, teknik ini dikenal sebagai *LSA* (*Latent Semantic Analysis*).

**Memilih *k*.** Kita pilih *k* berdasarkan grafik *scree* — kurva *variance explained* kumulatif terhadap jumlah komponen.

[GAMBAR 8.1]
Judul: Kurva varians kumulatif untuk memilih jumlah komponen (*scree plot*)
Tipe: plot data
Tampilkan: sumbu-x = jumlah komponen (1 hingga d), sumbu-y = proporsi varians kumulatif (0 hingga 1), dengan penanda titik siku (*elbow*) yang menunjukkan ambang ~95%
Sumber data: notebook Bab 8

Gambar 8.1 memperlihatkan pola khas: kurva naik cepat di komponen awal lalu mendatar. Titik siku (*elbow*) menandai titik di mana menambah komponen memberikan manfaat yang semakin kecil. Untuk visualisasi, kita cukup ambil $k=2$ atau $k=3$. Untuk pemodelan, lazimnya kita pilih $k$ yang menanggung sekitar 95% varians.

**Catatan praktis.** *PCA* sensitif terhadap skala fitur — fitur dengan rentang besar akan mendominasi. Karena itu, selalu *standardize* dulu menggunakan `StandardScaler` sebelum `PCA`. Untuk data *sparse* seperti matriks *term-document*, gunakan `TruncatedSVD` dari `sklearn.decomposition`. Perhatikan pula bahwa setiap *principal component* adalah kombinasi linear dari semua fitur asli, sehingga interpretabilitasnya terbatas dibanding fitur individual.

Satu batasan mendasar: kedua metode ini hanya menangkap struktur **linear**. Bila data membentuk manifold melengkung, teknik nonlinear seperti *t-SNE*, *UMAP*, atau *autoencoder* — yang dibahas di subseksi berikutnya — lebih tepat digunakan.

> **Posisi pada spektrum.** Komponen yang dihasilkan *PCA* bukan dirancang manusia secara eksplisit, melainkan diturunkan algoritma langsung dari data kita sendiri — ini berbeda dari *embedding* terlatih yang dipindahkan dari sumber lain (batas Ch 8 ↔ Ch 15). Representasi ini *dipelajari mesin* dari distribusi data kita, namun tidak membawa pengetahuan eksternal.

> **Disiplin *pipeline*.** Fit `PCA` atau `TruncatedSVD` **hanya pada data latih**, lalu terapkan transformasi yang sama ke data validasi dan uji. Menghitung komponen dari keseluruhan data sebelum pembagian adalah bentuk *leakage* yang umum terlewatkan.

---
