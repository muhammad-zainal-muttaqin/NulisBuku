# Blind Writer Evaluation - ch13_s05: Neighborhood aggregation and path-based features

Score each sample **1-5** on three dimensions (see the rubric):
**D1 Naturalness & correctness . D2 Register & accessibility . D3 Technical & terminological fidelity.**
Please do not try to guess which model wrote which sample.

## Sample 1

**13.5 Agregasi Lingkungan Tetangga dan Fitur Berbasis Lintasan**

Setelah menguasai fitur per-*node* seperti *degree*, *centrality*, dan *clustering coefficient* (subbab sebelumnya), kita sekarang melangkah ke deskripsi yang lebih kontekstual. Sebuah *node* dapat dipahami bukan hanya dari propertinya sendiri, melainkan dari karakteristik lingkungannya. Subbab ini mengenalkan dua keluarga fitur yang meringkas *neighborhood* dan *path*, yaitu cara menangkap konteks lokal *node* dalam *graph*.

**Agregasi Lingkungan Tetangga**

Intinya, nilai sebuah *node* sering tercermin pada tetangganya. Dalam *graph* transaksi keuangan, risiko sebuah akun bisa diperkirakan dari rata-rata risiko akun-akun yang bertransaksi langsung dengannya (*1-hop neighborhood*). Kita hitung agregat—rata-rata, jumlah, atau maksimum—dari fitur tetangga tersebut. Kita juga bisa meluas ke *2-hop neighborhood* (tetangga dari tetangga) untuk menangkap pengaruh tidak langsung. Perbedaan antara rata-rata risiko di lingkungan 1-hop dan 2-hop bisa mengungkap apakah akun tersebut berada di pusar aktivitas berisiko tinggi atau sekadar di pinggirannya.

Ini adalah *neighborhood aggregation*: meringkas atribut *node* di sekitar target menjadi satu vektor fitur. Kita tentukan sendiri fungsi agregasinya (*mean*, *sum*, atau *max*) dan seberapa jauh jangkauannya (*k-hop*). Hasilnya eksplisit dan dapat diinterpretasi, sebab setiap dimensi memiliki arti yang kita tetapkan.

**Fitur Berbasis Lintasan**

Selain agregasi, kita bisa membaca *graph* melalui *path*. Salah satu pendekatan adalah menghitung *shortest-path distance* dari *node* target ke *node* landmark tertentu. Dalam *graph* sosial, jarak ke akun berpengaruh bisa jadi fitur penting. Kita juga bisa menghitung partisipasi *node* dalam *motif* struktural, seperti segitiga (*triangle*) atau pola koneksi kecil lainnya, yang sering mengindikasikan fungsi spesifik dalam jaringan.

**Batasan dan Motivasi**

Kedua keluarga fitur ini kita tentukan sendiri: kita yang memilih tetangga mana yang diagregasi, *path* mana yang diukur, dan *motif* mana yang dihitung. Keterbatasan ini justru menjadi pendorong subbab berikutnya. Ketika struktur *graph* semakin kompleks, menentukan agregasi manual menjadi tidak praktis. Subbab 13.6 akan mengantarkan representasi yang *dipelajari mesin*—di mana model sendiri yang mempelajari cara mengagregasi informasi dari lingkungan.

**Catatan Praktik *Pipeline***

Perhitungan fitur lingkungan harus dilakukan hanya pada *training split* untuk menghindari *leakage*. Jika kita menghitung agregasi di seluruh *graph* sebelum memisah data, informasi dari *validation* atau *test set* bisa terserap ke dalam fitur *training*. Masalah ini akan dibahas mendalam di subbab 13.8.

---

## Sample 2

### Agregasi *Neighborhood* dan Fitur Berbasis *Path*

Pada subbab sebelumnya, kita telah melihat bagaimana fitur seperti derajat dan sentralitas menangkap karakteristik individual sebuah *node*. Namun, dalam struktur graf, identitas sebuah *node* sering kali lebih baik dijelaskan oleh lingkungan di sekitarnya, bukan hanya oleh dirinya sendiri. Di sinilah kita memanfaatkan agregasi *neighborhood* dan fitur berbasis *path*.

Agregasi *neighborhood* bertujuan untuk meringkas atribut tetangga sebuah *node* menjadi fitur. Proses ini biasanya melibatkan operasi statistik sederhana seperti rata-rata, penjumlahan, atau nilai maksimum pada atribut *node* yang berada dalam *k-hop neighborhood*, yaitu himpunan *node* yang dapat dicapai dalam *k* langkah. Sebagai contoh, dalam sebuah graf transaksi keuangan, kita dapat meringkas profil risiko sebuah akun dengan menghitung rata-rata skor risiko dari tetangga langsungnya (1-*hop*), lalu membandingkannya dengan rata-rata risiko dari tetangga yang berjarak dua langkah (2-*hop*). Kontras antara lingkaran pertama dan kedua ini sering kali memberikan sinyal prediktif yang kuat mengenai aktivitas yang mencurigakan.

Selain meringkas atribut tetangga, kita juga dapat mengekstraksi *path-based feature*, yakni fitur yang dihitung dari lintasan pada graf. Contoh umum meliputi metrik ketercapaian, jarak *shortest-path* ke *node* referensi tertentu, serta seberapa sering sebuah *node* terlibat dalam pola struktur kecil atau *motif* (seperti formasi segitiga). Fitur-fitur ini memberikan konteks topologis yang lebih luas dibandingkan sekadar melihat tetangga terdekat.

Perlu diperhatikan bahwa menghitung fitur-fitur yang bergantung pada struktur graf ini memerlukan kehati-hatian. Melakukan agregasi pada seluruh graf sebelum memisahkan data latih dan data uji dapat menyebabkan kebocoran informasi (*leakage*), karena struktur dari data uji ikut memengaruhi nilai fitur pada data latih. Kita akan membahas mitigasi masalah ini lebih lanjut pada Subbab 13.8.

Walaupun agregasi dan penghitungan *path* ini sangat eksplisit dan mudah diinterpretasi, pendekatan ini memiliki batas. Kita harus memilih dan menentukan sendiri metrik apa yang akan dihitung. Ketika menghadapi struktur graf yang sangat kaya dan kompleks, menentukan kombinasi agregasi secara manual menjadi tidak efisien. Keterbatasan inilah yang menjadi motivasi untuk langkah berikutnya: membiarkan model mempelajari sendiri representasi *node* yang paling optimal dari struktur graf tersebut.

---

## Sample 3

### 13.5 Agregasi Tetangga dan Fitur Berbasis Lintasan

Fitur per-*node* seperti derajat dan sentralitas (Subbab 13.4) hanya menggambarkan *node* itu sendiri. Untuk menangkap konteks yang lebih kaya, kita perlu mencirikan *node* berdasarkan lingkungan sekitarnya. Dua pendekatan yang umum adalah agregasi tetangga (*neighborhood aggregation*) dan fitur berbasis lintasan (*path-based feature*).

Agregasi tetangga meringkas atribut dari *node*-*node* yang terhubung langsung ke *node* target. Kita dapat menghitung rata-rata, jumlah, atau nilai maksimum suatu atribut (misalnya skor risiko atau kategori) dari tetangga 1-*hop*. Ekspansi ke 2-*hop* (himpunan *node* yang dapat dicapai dalam dua langkah) memberikan perspektif yang lebih luas. Pada graf transaksi, sebuah *node* mungkin dikelilingi oleh tetangga langsung dengan risiko tinggi, tetapi tetangga 2-*hop*-nya sebagian besar berisiko rendah. Perbedaan ini menjadi sinyal penting yang tidak terlihat dari statistik *node* tunggal. Agregasi dapat diterapkan pada atribut kontinu (seperti rata-rata usia akun) maupun diskret (seperti modus label).

Fitur berbasis lintasan mengeksploitasi jalur di dalam graf. Contoh klasik adalah partisipasi *motif*: berapa banyak segitiga yang melibatkan *node* tersebut, yang setara dengan menghitung lintasan tertutup sepanjang dua langkah. Fitur ini menangkap kohesi lokal dengan cara yang berbeda dari koefisien *clustering*. Selain itu, kita dapat menggunakan jarak *shortest-path* ke sekumpulan *node* penanda (*landmark*), misalnya jarak ke beberapa *node* pusat, sebagai vektor fitur. Informasi keterjangkauan (*reachability*) juga dapat dihitung: apakah *node* A dapat mencapai *node* B dalam *k* langkah?

Semua fitur ini masih dirancang secara manual: kita memutuskan agregasi mana yang dihitung dan lintasan mana yang diukur. Keunggulannya adalah interpretabilitas tinggi—kita tahu persis apa yang direpresentasikan. Namun, pendekatan ini tidak berskala untuk menangkap pola struktural yang kompleks karena kita hanya bisa menghitung apa yang sudah kita pikirkan. Keterbatasan inilah yang memotivasi pergeseran ke arah representasi yang dipelajari mesin, yang akan dibahas mulai Subbab 13.6.

Satu catatan penting: menghitung fitur-fitur ini pada seluruh graf sebelum memisahkan data latih dan uji dapat menyebabkan kebocoran struktural karena informasi dari *test set* merembes ke *train set* melalui koneksi graf. Isu ini akan diuraikan secara mendalam di Subbab 13.8.

---
