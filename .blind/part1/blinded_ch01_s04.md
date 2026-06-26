# Blind Writer Evaluation - ch01_s04: The myth "feature engineering is dead in deep learning"

Score each sample **1-5** on three dimensions (see the rubric):
**D1 Naturalness & correctness . D2 Register & accessibility . D3 Technical & terminological fidelity.**
Please do not try to guess which model wrote which sample.

## Sample 1

### 1.4 Mitos "Rekayasa Fitur Telah Mati di Era *Deep Learning*"

Ada klaim populer di kalangan praktisi *machine learning* bahwa kemunculan *deep learning* menandai akhir dari rekayasa fitur. Argumennya terdengar masuk akal: karena jaringan saraf tiruan yang dalam mampu mengekstraksi representasi secara otomatis dari data mentah, peran manusia dalam merancang fitur dianggap tidak lagi relevan. Namun, anggapan ini adalah sebuah mitos.

Rekayasa fitur sama sekali tidak mati; ia hanya bergeser sepanjang spektrum dari representasi yang *dirancang manusia* menuju representasi yang *dipelajari mesin*. Alih-alih saling menggantikan, kedua ujung spektrum ini justru saling melengkapi. Pada banyak aplikasi dunia nyata, solusi hibrida yang memadukan keduanya sering kali menjadi pilihan paling optimal.

Sebagai ilustrasi, bayangkan sebuah sistem klasifikasi teks. Kita dapat membandingkan tiga pendekatan: pertama, hanya menggunakan fitur tradisional yang *dirancang manusia* (seperti frekuensi kata atau rasio kalimat tanya); kedua, hanya menggunakan *embedding* dari model *pretrained* yang *dipelajari mesin*; dan ketiga, menggabungkan keduanya. Dalam banyak kasus praktis, model hibrida yang memadukan fitur hasil rancangan manusia dengan *embedding* tersebut mampu mengungguli kedua pendekatan tunggal. Fitur buatan manusia menangkap pola spesifik domain atau aturan bisnis yang mungkin terlewat oleh representasi otomatis, sementara *embedding* menangkap konteks semantik yang kaya.

Bahkan ketika arsitektur *deep learning* sangat dalam, kita tetap harus merancang representasi input awal, menentukan strategi tokenisasi, merancang augmentasi data, dan memutuskan fitur mana yang perlu disuntikkan bersamaan dengan fitur yang dipelajari model. Keterampilan seorang praktisi kini bergeser dari merancang fitur secara manual menjadi memilih, menggabungkan, dan memvalidasi berbagai representasi.

Pergeseran keterampilan ini, beserta teknik otomatisasi dan rekayasa fitur modern yang menyertainya, akan kita bahas lebih mendalam pada Bab 15. Sebagai penutup bab ini dan pengantar menuju Bab 16, kita perlu menyadari bahwa rekayasa fitur modern bukan tentang memilih secara kaku antara campur tangan manusia atau otomatisasi mesin. Ini adalah tentang orkestrasi keduanya untuk membangun representasi data yang paling kaya dan model yang paling efektif.

---

## Sample 2

### 1.4 Mitos "Rekayasa Fitur Telah Mati dalam *Deep Learning*"

Seiring dengan kepopuleran *deep learning*, muncul sebuah anggapan yang sering kita dengar: rekayasa fitur sudah tidak lagi relevan. Argumen ini mengasumsikan bahwa karena jaringan saraf tiruan mampu mengekstraksi fiturnya sendiri secara otomatis dari data mentah, praktisi *machine learning* tidak perlu lagi repot merumuskan fitur. Pandangan ini menciptakan mitos bahwa era rekayasa fitur telah berakhir.

Kenyataannya, rekayasa fitur sama sekali tidak mati. Praktik ini hanya bergeser di sepanjang spektrum yang telah kita bahas sebelumnya. Alih-alih hilang, fokus kita berpindah dari representasi yang *dirancang manusia* menuju representasi yang *dipelajari mesin*. Dalam paradigma baru ini, mesin memang mengambil alih sebagian besar beban ekstraksi pola, tetapi keputusan awal mengenai bentuk data yang diberikan ke dalam model tetap berada di tangan kita.

Meskipun kita menggunakan arsitektur *deep learning* yang sangat kompleks, cara kita merepresentasikan input tetap menjadi penentu utama keberhasilan. Proses seperti tokenisasi teks, augmentasi citra, atau penyesuaian format input pada dasarnya adalah bentuk rekayasa fitur. Kita akan mengeksplorasi lebih jauh pada Bab 15 bahwa rekayasa fitur modern justru sering menyuapkan fitur yang dirumuskan secara spesifik berdampingan dengan fitur otomatis.

Dalam praktiknya, pendekatan hibrida sangat umum dan terbukti efektif. Sebagai contoh, mari kita tinjau sebuah sistem rekomendasi produk. Jika kita hanya mengandalkan fitur statistik pengguna seperti rata-rata transaksi, model mungkin kesulitan menangkap selera pengguna yang lebih abstrak. Di sisi lain, jika kita murni hanya menggunakan sebuah *pretrained embedding* dari teks ulasan pengguna, model bisa saja kehilangan sinyal perilaku numerik yang sederhana namun kuat. Namun, ketika kita menggabungkan fitur statistik tersebut sebagai representasi yang *dirancang manusia* bersama dengan *pretrained embedding* sebagai representasi yang *dipelajari mesin*, model sering kali menghasilkan performa yang jauh melampaui penggunaan salah satu metode secara terpisah.

Oleh karena itu, keahlian kita tidak menjadi usang. Keterampilan tersebut hanya berevolusi dari sekadar memahat fitur secara manual menjadi kemampuan untuk memilih, menggabungkan, dan memvalidasi berbagai bentuk representasi. Representasi yang *dirancang manusia* dan representasi yang *dipelajari mesin* bukanlah dua hal yang saling bersaing. Keduanya justru saling melengkapi untuk membangun model yang lebih tangguh dan akurat.

---

## Sample 3

### Mitos: Rekayasa Fitur Mati karena *Deep Learning*

Salah satu anggapan yang sering muncul adalah bahwa rekayasa fitur sudah tidak diperlukan karena *deep learning* dapat membentuk fiturnya sendiri. Anggapan ini masuk akal sekilas, terutama jika kita membandingkan model lama yang bergantung pada fitur buatan manusia dengan jaringan modern yang menerima citra, teks, atau audio dalam bentuk lebih mentah. Namun, kesimpulan “rekayasa fitur sudah mati” terlalu cepat.

Dengan istilah yang sudah kita pakai pada bagian sebelumnya, yang terjadi bukanlah kematian rekayasa fitur, melainkan pergeseran posisi pada sumbu *dirancang manusia ↔ dipelajari mesin*. Pada banyak sistem modern, sebagian representasi memang dipelajari mesin dari data. Tetapi manusia masih menentukan banyak hal penting: bentuk masukan yang diberikan ke model, cara teks dipecah melalui *tokenization*, strategi *augmentation*, serta fitur tambahan yang mungkin digabungkan dengan representasi dari jaringan.

Bayangkan sebuah sistem klasifikasi teks. Kita dapat mencoba tiga rancangan. Pertama, model hanya memakai fitur yang dirancang manusia, misalnya statistik sederhana dari dokumen. Kedua, model hanya memakai *pretrained embedding*. Ketiga, model menggabungkan keduanya: *embedding* memberi representasi semantik yang kaya, sementara fitur yang dirancang manusia menangkap sinyal sederhana yang tetap berguna. Dalam praktik, rancangan hibrida seperti ini dapat mengungguli dua rancangan yang berdiri sendiri, bukan karena salah satunya “lebih modern”, melainkan karena keduanya menangkap sisi informasi yang berbeda.

**Catatan spektrum.** Bagian ini berada di tengah sumbu *dirancang manusia ↔ dipelajari mesin*. Rekayasa fitur modern tidak selalu berarti kita menulis semua fitur dengan tangan, dan juga tidak berarti kita menyerahkan seluruh representasi kepada model. Keterampilannya bergeser: dari sekadar membuat fitur satu per satu menjadi memilih, menggabungkan, dan memvalidasi representasi.

Karena itu, *deep learning* tidak menghapus rekayasa fitur. Ia mengubah bentuk pekerjaannya. Dalam *machine learning* modern, pertanyaan yang lebih tepat bukan “apakah fitur dibuat manusia atau mesin?”, melainkan “kombinasi representasi mana yang paling sesuai, stabil, dan bermanfaat untuk tujuan model?” Gagasan ini akan muncul kembali ketika kita membahas rekayasa fitur modern dan otomatis pada Bab 15, lalu menjadi bagian dari tesis penutup buku ini pada Bab 16.

---

## Sample 4

## Mitos “Rekayasa Fitur Sudah Mati dalam *Deep Learning*”

Banyak yang berpendapat bahwa *deep learning* telah mengakhiri rekayasa fitur. Karena model *deep learning* mampu mempelajari representasinya sendiri, maka tugas merancang fitur secara manual dianggap tidak relevan lagi. Pandangan ini terlalu sederhana.

Rekayasa fitur tidak hilang; ia bergeser sepanjang sumbu *dirancang manusia ↔ dipelajari mesin*. Pada satu ujung, manusia masih menentukan bagaimana data mentah diubah menjadi bentuk yang dapat diterima model, misalnya melalui tokenisasi teks, normalisasi citra, atau augmentasi data. Pada ujung lain, lapisan-lapisan jaringan saraf mengubah representasi tersebut menjadi fitur yang semakin abstrak. Di antara keduanya, kombinasi kedua pendekatan justru sering memberikan hasil terbaik.

Bayangkan sebuah tugas klasifikasi dokumen. Kita dapat menggunakan *pretrained embedding* yang sudah dipelajari mesin dari korpus besar, lalu menambahkan beberapa fitur yang dirancang manusia, seperti panjang dokumen, rasio tanda baca, atau frekuensi kata kunci domain tertentu. Ketika fitur hasil rancangan manusia digabungkan dengan *embedding*, performa model biasanya lebih baik daripada hanya menggunakan salah satu saja. Kombinasi ini menunjukkan bahwa *dirancang manusia* dan *dipelajari mesin* bersifat saling melengkapi, bukan bersaing.

Keterampilan yang dibutuhkan pun berubah. Alih-alih merancang setiap fitur dari nol, praktisi kini lebih banyak memilih, menggabungkan, dan memvalidasi berbagai representasi yang tersedia. Keputusan tentang representasi input, strategi augmentasi, serta cara menggabungkan fitur yang dipelajari dengan fitur yang dirancang manusia tetap memengaruhi kualitas model secara signifikan.

Pergeseran ini akan dibahas lebih lanjut pada Bab 15, ketika kita meninjau teknik rekayasa fitur otomatis dan hibrida yang semakin umum digunakan.

---

## Sample 5

### 1.4 Mitos “Rekayasa Fitur Sudah Mati di Era *Deep Learning*”

Salah satu klaim yang sering terdengar sejak kebangkitan *deep learning* adalah bahwa rekayasa fitur tidak lagi diperlukan. Argumennya sederhana: *deep learning* mampu mempelajari representasi secara otomatis dari data mentah, sehingga campur tangan manusia dalam merancang fitur menjadi usang. Klaim ini mengandung setengah kebenaran yang berbahaya—ia mengabaikan bahwa yang berubah bukanlah hilangnya rekayasa fitur, melainkan **letaknya pada spektrum** *dirancang manusia ↔ dipelajari mesin*.

Ketika kita melatih model *deep learning* pada citra atau teks, benar bahwa lapisan-lapisan jaringan mengekstrak fitur secara hierarkis tanpa kita menuliskan detektor tepi atau aturan tata bahasa secara eksplisit. Namun, sebelum data menyentuh jaringan, serangkaian keputusan representasi tetap harus diambil manusia: bagaimana teks dipecah menjadi token (*tokenization*), apakah citra diubah ukurannya atau diperkaya dengan augmentasi, dan apakah fitur-fitur terstruktur (seperti metrik domain atau statistik agregat) perlu disertakan bersama data mentah. Keputusan-keputusan ini adalah bentuk rekayasa fitur modern yang bergeser dari perancangan manual menuju pemilihan, penggabungan, dan validasi representasi.

Contoh paling jelas terlihat pada pendekatan hibrida. Misalkan kita membangun pengklasifikasi sentimen untuk ulasan produk. Kita dapat memanfaatkan *embedding* teks dari model *pretrained* (representasi yang sepenuhnya *dipelajari mesin*), lalu menggabungkannya dengan fitur-fitur yang *dirancang manusia* seperti panjang kalimat, jumlah kata bermuatan emosi, atau skor keterbacaan. Model hibrida semacam ini acap kali mengungguli model yang hanya mengandalkan *embedding* saja atau fitur buatan tangan saja. Di sini, kedua ujung spektrum saling melengkapi, bukan bersaing.

Dengan demikian, keterampilan yang bergeser bukan berarti menghilang. Praktisi tidak lagi menghabiskan waktu merancang setiap fitur secara atomik, tetapi justru harus mampu memilih representasi yang tepat, mengombinasikan sumber-sumber representasi yang berbeda, serta memvalidasi apakah representasi yang dipelajari mesin benar-benar menangkap struktur yang relevan dengan tugas. Inilah inti dari rekayasa fitur modern yang akan kita jelajahi lebih dalam pada Bab 15, ketika kita membahas otomatisasi dan pemilihan representasi.

Pada akhirnya, *dirancang manusia* dan *dipelajari mesin* bukanlah dua kutub yang saling meniadakan. Keduanya hidup berdampingan dalam hampir setiap sistem *machine learning* yang berhasil. Mitos bahwa rekayasa fitur telah mati justru menutupi kenyataan bahwa ia telah bertransformasi—dan tetap menjadi jantung dari performa model.

---

## Sample 6

## 1.4 Mitos "Rekayasa Fitur Mati di Era *Deep Learning*"

Klaim ini terdengar meyakinkan: karena *deep learning* mampu mempelajari representasinya sendiri langsung dari data mentah, rekayasa fitur tidak lagi diperlukan. Para praktisi cukup menyuplai piksel, teks, atau sinyal mentah, lalu biarkan model bekerja sendiri. Rekayasa fitur, konon, adalah urusan masa lalu.

Klaim ini separuh benar — dan justru di bagian yang salah itulah banyak proyek gagal.

Yang sebenarnya terjadi bukan kematian, melainkan **pergeseran posisi pada spektrum** yang sudah kita kenal dari subbab sebelumnya. Ingat kembali sumbu *representasi yang dirancang manusia* di satu ujung dan *representasi yang dipelajari mesin* di ujung lain. *Deep learning* memang menggeser banyak pekerjaan ke arah kutub *dipelajari mesin* — lapisan konvolusi, mekanisme *attention*, dan *autoencoder* semuanya belajar merepresentasikan data tanpa campur tangan manusia secara eksplisit. Namun pergeseran sumbu itu tidak menghapus sisi *dirancang manusia*; ia justru memperkaya ruang hibrida di antara keduanya.

Ambil satu contoh yang sering dijumpai dalam praktik: sebuah tim membangun model prediksi risiko kredit. Mereka mencoba dua pendekatan, pertama hanya menggunakan *pretrained embedding* dari narasi pengajuan pinjaman, kedua hanya menggunakan fitur yang dirancang manusia seperti rasio utang, riwayat keterlambatan, dan stabilitas pekerjaan. Keduanya menghasilkan performa yang memadai, tetapi tidak istimewa. Ketika fitur yang dirancang manusia digabungkan bersama *embedding* tersebut ke dalam satu model, hasilnya melampaui kedua pendekatan sebelumnya secara konsisten. Tidak ada angka ajaib di sini — melainkan pola yang berulang: representasi yang *dirancang manusia* dan yang *dipelajari mesin* membawa informasi yang saling melengkapi, bukan bersaing.

Bahkan dalam arsitektur *deep learning* paling modern pun, manusia masih membuat keputusan penting: bagaimana teks di-*tokenize*, augmentasi apa yang diterapkan pada citra, fitur tabular mana yang disertakan bersama *embedding*, dan apakah skala atau distribusi input perlu disesuaikan sebelum masuk ke jaringan. Keputusan-keputusan inilah yang membentuk input, dan input yang buruk tetap menghasilkan model yang buruk — tidak peduli seberapa dalam arsitekturnya.

Dengan demikian, keahlian yang bergeser bukanlah keahlian yang hilang. Praktisi tidak lagi perlu *merancang tangan* setiap fitur, tetapi kini dituntut untuk **memilih, memadukan, dan memvalidasi** representasi dari berbagai sumber. Cara melakukan itu secara sistematis dan otomatis akan menjadi fokus Bab 15, dan implikasinya bagi praktik rekayasa fitur modern akan ditarik sebagai benang merah penutup di Bab 16.

---
