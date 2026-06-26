# Blind Writer Evaluation - ch01_s03: Designed vs. learned representations  *(defines the spine + requires a figure)*

Score each sample **1-5** on three dimensions (see the rubric):
**D1 Naturalness & correctness . D2 Register & accessibility . D3 Technical & terminological fidelity.**
Please do not try to guess which model wrote which sample.

## Sample 1

### 1.3 Representasi yang Dirancang Manusia vs. Dipelajari Mesin

Pada subbab sebelumnya, kita telah menyepakati bahwa kualitas representasi menentukan batas atas performa sebuah model. Kini kita sampai pada pertanyaan mendasar yang menjadi sumbu utama buku ini: siapa yang menghasilkan bentuk representasi tersebut? Secara konseptual, pendekatan rekayasa fitur berada di antara dua kutub, yaitu representasi yang **dirancang manusia** dan representasi yang **dipelajari mesin**.

Pada kutub *dirancang manusia*, bentuk representasi ditentukan secara eksplisit oleh manusia. Kita merancang transformasi atau mendefinisikan fitur tersebut, baik dengan menulisnya secara langsung maupun melalui *pipeline automated feature engineering*. Hasil akhirnya adalah fitur yang eksplisit dan mudah diinterpretasikan. Sebaliknya, pada kutub *dipelajari mesin*, bentuk representasi dibentuk oleh model secara langsung dari data selama proses pelatihan. Pendekatan ini menghasilkan representasi yang implisit dan terdistribusi, seperti *word embedding* atau fitur laten dari sebuah *autoencoder*.

Perlu kita tegaskan dua hal di sini. Pertama, kata "dipelajari" secara spesifik merujuk pada mesin, bukan pada kita yang mempelajari data. Kedua, otomasi tidak otomatis mengubah suatu pendekatan menjadi *dipelajari mesin*. Sebuah *pipeline automated feature engineering* memang mengeksekusi pencarian fitur secara otomatis, tetapi ruang pencarian dan aturan transformasinya tetap *dirancang manusia*.

[GAMBAR 1.1]
Judul: Spektrum representasi dari dirancang manusia hingga dipelajari mesin
Tipe: diagram konseptual
Tampilkan: sebuah kontinum horizontal. Ujung kiri berlabel *dirancang manusia* dengan contoh teknik (*one-hot*, rasio, *target encoding*, *automated feature engineering*). Ujung kanan berlabel *dipelajari mesin* dengan contoh (*word embedding*, *autoencoder*, GNN). Bagian tengah berlabel *hybrid*. Sumbu utama menunjukkan pihak yang menghasilkan representasi (manusia ke mesin).
Sumber data: ->

Gambar 1.1 memperlihatkan bahwa kedua kutub ini bukanlah dua kotak yang terpisah, melainkan sebuah spektrum atau kontinum. Kita dapat menempatkan berbagai teknik di sepanjang garis ini. Sebagai contoh, *one-hot encoding* dan *target encoding* berada sangat dekat dengan ujung *dirancang manusia* karena aturannya ditetapkan sepenuhnya oleh praktisi. Di ujung yang berlawanan, *word embedding* yang dilatih dari awal berada di wilayah *dipelajari mesin*. Di area tengah, kita menemukan pendekatan *hybrid*, misalnya ketika kita menggabungkan *pretrained embedding* dengan fitur rasio yang direkayasa secara tradisional.

Posisi sebuah teknik pada spektrum ini membawa konsekuensi praktis yang nyata. Representasi yang *dirancang manusia* umumnya membutuhkan lebih sedikit data dan sangat mudah diinterpretasikan, tetapi membutuhkan intuisi dan upaya perancangan yang besar dari praktisi. Di sisi lain, representasi yang *dipelajari mesin* dapat menangkap pola yang sangat kompleks, namun menuntut volume data yang besar, biaya komputasi yang tinggi, dan mengorbankan interpretabilitas. Pemahaman terhadap spektrum ini akan terus kita gunakan di sepanjang buku untuk menavigasi berbagai pilihan desain.

---

## Sample 2

### 1.3 Representasi yang Dirancang Manusia vs. Dipelajari Mesin

Kita telah memahami bahwa kualitas representasi menentukan batas maksimal dari performa model. Pertanyaan mendasar berikutnya adalah mengenai asal-usul representasi tersebut: siapa yang menentukan bentuk akhirnya? Dalam *machine learning* modern, pendekatan ini berpusat pada sebuah sumbu utama, yaitu apakah representasi tersebut *dirancang manusia* atau *dipelajari mesin*.

Pada representasi yang *dirancang manusia*, bentuk representasi ditentukan manusia. Kita sebagai praktisi merumuskan secara spesifik bagaimana data mentah diubah menjadi fitur yang berguna. Hasil dari pendekatan ini adalah sekumpulan fitur yang eksplisit dan mudah diinterpretasikan. Penting untuk dicatat bahwa otomatisasi tidak secara otomatis mengubah sifat ini. Meskipun kita menggunakan sistem *automated feature engineering* untuk menghasilkan ribuan fitur dengan cepat, aturan dan transformasi dasarnya tetap berakar pada logika yang dirumuskan oleh manusia.

Sebaliknya, pada representasi yang *dipelajari mesin*, bentuk representasi dibentuk model dari data selama proses pelatihan. Kata "dipelajari" di sini secara tegas merujuk pada mesin, bukan kita sebagai manusia yang mempelajarinya. Model akan menemukan sendiri pola terbaik untuk merepresentasikan data. Hasilnya sering kali berupa representasi yang implisit dan terdistribusi di dalam jaringan model.

[GAMBAR 1.1]
Judul: Spektrum representasi dari yang dirancang manusia hingga dipelajari mesin.
Tipe: diagram konseptual
Tampilkan: Sebuah kontinum horizontal. Ujung kiri berlabel 'dirancang manusia' dengan contoh teknik (one-hot, rasio, target encoding, automated feature engineering). Ujung kanan berlabel 'dipelajari mesin' dengan contoh (word embedding, autoencoder, GNN). Bagian tengah berlabel 'hybrid'. Sumbu utama menunjukkan siapa yang memproduksi representasi (manusia → mesin).
Sumber data: -

Gambar 1.1 memperlihatkan bahwa kedua kutub ini sebenarnya membentuk sebuah spektrum atau kontinum, bukan dua kategori biner yang terpisah kaku. Posisi sebuah teknik pada spektrum ini menunjukkan seberapa besar peran manusia dibandingkan dengan mesin dalam memproduksi representasi tersebut. 

Di ujung paling kiri spektrum, kita menemukan teknik seperti *one-hot* atau *target encoding* yang sepenuhnya dikendalikan oleh manusia. Di ujung paling kanan, terdapat teknik seperti *word embedding* atau representasi dari *autoencoder* yang sepenuhnya diserahkan kepada model. Di antara keduanya, kita sering menemukan pendekatan hibrida. Sebagai contoh, kita dapat mengambil *pretrained embedding* yang dihasilkan oleh model *deep learning*, lalu menggabungkannya dengan fitur-fitur yang dirancang secara cermat oleh manusia untuk menyelesaikan masalah bisnis tertentu.

Posisi pada kontinum ini membawa konsekuensi praktis. Semakin dekat sebuah representasi ke kutub *dirancang manusia*, sistem cenderung lebih mudah diinterpretasikan, lebih murah secara komputasi, dan membutuhkan lebih sedikit data. Sebaliknya, semakin bergeser ke arah *dipelajari mesin*, kita berpotensi menangkap pola yang jauh lebih kompleks, namun harus menukarnya dengan kebutuhan data yang masif, biaya komputasi yang tinggi, dan menurunnya transparansi model.

---

## Sample 3

### Representasi yang dirancang manusia dan dipelajari mesin

Pada subbagian sebelumnya, kita melihat bahwa representasi memberi batas atas bagi apa yang dapat dipelajari model. Sumbu utama buku ini berangkat dari pertanyaan sederhana: siapa yang menentukan bentuk representasi itu?

Representasi yang **dirancang manusia** berarti bentuk representasi ditentukan manusia. Manusia menetapkan transformasi, memilih fitur, atau menyusun *pipeline* yang menghasilkan fitur, termasuk ketika sebagian langkahnya otomatis. Hasilnya biasanya eksplisit dan mudah diperiksa: kategori diubah menjadi kolom indikator, atau dua nilai numerik digabung menjadi rasio.

Representasi yang **dipelajari mesin** berarti bentuk representasi dibentuk model dari data selama pelatihan. Manusia tidak merinci fitur satu per satu; model membangun pola internalnya sendiri, seperti vektor pada *embedding* atau fitur laten pada *autoencoder*. Representasi ini cenderung implisit dan tersebar: makna suatu pola muncul dari kombinasi banyak dimensi, bukan dari satu kolom yang langsung dapat dinamai.

[GAMBAR 1.1]  
Judul: Spektrum representasi dari dirancang manusia ke dipelajari mesin  
Tipe: diagram konseptual  
Tampilkan: Kontinum horizontal. Ujung kiri berlabel *dirancang manusia* dengan contoh *one-hot*, rasio, *target encoding*, dan *automated FE*. Ujung kanan berlabel *dipelajari mesin* dengan contoh *word embedding*, *autoencoder*, dan GNN. Bagian tengah berlabel *hybrid*. Sumbu diberi keterangan: siapa yang membentuk representasi, dari manusia menuju mesin.  
Sumber data: -

Gambar 1.1 perlu dibaca sebagai spektrum atau kontinum, yaitu rentang berkelanjutan antara dua ujung, bukan dua kotak terpisah. Untuk menempatkan sebuah teknik, tanyakan: siapa yang menentukan bentuk akhirnya? *One-hot* berada dekat ujung dirancang manusia karena manusia menetapkan aturan bahwa kategori menjadi kolom-kolom indikator. *Word embedding* berada dekat ujung dipelajari mesin karena posisi kata dalam ruang vektor dibentuk dari data selama pelatihan. Sementara itu, sistem yang memakai *pretrained embedding* sekaligus fitur rasio yang dirancang manusia berada di tengah sebagai pendekatan *hybrid*.

Ada dua salah paham yang perlu kita hindari sejak awal. Pertama, ungkapan **dipelajari mesin** harus dibaca utuh: yang membentuk representasi adalah mesin, bukan kita sebagai pembaca. Kedua, otomatisasi saja tidak membuat suatu teknik menjadi dipelajari mesin. *Automated FE* memang otomatis mencoba banyak transformasi, tetapi ruang pencarian dan bentuk kandidatnya masih diarahkan manusia, sehingga posisinya tetap dekat dengan dirancang manusia.

Posisi pada spektrum ini berpengaruh pada interpretabilitas, kebutuhan data, dan biaya. Fitur yang dirancang manusia sering lebih mudah dijelaskan, tetapi menuntut keahlian manusia. Representasi yang dipelajari mesin dapat menangkap pola yang lebih sulit dirumuskan, tetapi biasanya memerlukan data dan biaya pelatihan yang lebih besar.

---

## Sample 4

Representasi yang Dirancang Manusia versus yang Dipelajari Mesin

Inti bab ini terletak pada satu pertanyaan sederhana: siapa yang menentukan bentuk representasi? Jawabannya membentuk sumbu utama buku ini, yaitu spektrum antara representasi yang dirancang manusia dan representasi yang dipelajari mesin.

Pada ujung kiri, manusia yang menetapkan transformasi. Ia bisa menulis aturan secara langsung atau menyusun pipeline otomatis; yang penting, bentuk fitur akhir tetap ditentukan oleh manusia. Hasilnya berupa fitur yang eksplisit dan mudah diinterpretasi, misalnya *one-hot encoding*, rasio dua kolom, atau *target encoding*. Semua teknik ini tetap berada di sisi *dirancang manusia* meskipun sebagian langkahnya diotomasi.

Pada ujung kanan, model yang membentuk representasi dari data selama pelatihan. Bentuk akhir tidak lagi ditentukan manusia, melainkan muncul sebagai hasil optimisasi. Representasi ini biasanya tersebar (*distributed*) dan sukar ditafsirkan secara langsung, seperti *embedding* kata pada model bahasa atau fitur laten yang dihasilkan *autoencoder*.

Kedua kutub tersebut bukan kotak terpisah, melainkan sebuah kontinum. Di tengah-tengah terdapat banyak posisi hibrida: *embedding* yang sudah dilatih sebelumnya kemudian digabungkan dengan beberapa fitur rekayasa tangan, misalnya. Posisi suatu teknik pada spektrum ini memengaruhi beberapa hal praktis: seberapa mudah kita memahami keputusan model, berapa banyak data yang diperlukan, serta biaya komputasi yang harus dikeluarkan.

Gambar 1.1 memperlihatkan spektrum tersebut secara visual.

[GAMBAR 1.1]
Judul: Spektrum representasi: dari yang dirancang manusia hingga yang dipelajari mesin
Tipe: diagram konseptual
Tampilkan: garis horizontal kontinu; ujung kiri berlabel “dirancang manusia” dengan contoh teknik (one-hot, rasio, target encoding, automated FE); ujung kanan berlabel “dipelajari mesin” dengan contoh (word embedding, autoencoder, GNN); bagian tengah berlabel “hybrid”; sumbu bawah bertuliskan “siapa yang menghasilkan representasi (manusia → mesin)”

Untuk membaca gambar ini, perhatikan posisi setiap teknik relatif terhadap kedua ujung. Semakin dekat suatu teknik ke kiri, semakin besar peran manusia dalam menentukan bentuk fitur. Semakin dekat ke kanan, semakin besar peran model dalam membentuk representasi selama pelatihan. Posisi hibrida menunjukkan kombinasi keduanya.

Pembaca sudah mengetahui bahwa kualitas representasi menentukan batas atas kinerja model. Bab ini menegaskan bahwa batas tersebut juga bergantung pada siapa yang merancang representasi tersebut. Diskusi selanjutnya akan selalu merujuk kembali ke posisi teknik yang dibahas pada spektrum ini.

---

## Sample 5

## 1.3 Representasi yang Dirancang Manusia dan yang Dipelajari Mesin

Saat membangun model, satu pertanyaan mendasar selalu muncul: siapa yang menentukan bentuk representasi yang akan digunakan? Apakah kita sebagai manusia yang merancang fitur secara eksplisit, ataukah model yang membentuk representasi dari data selama pelatihan? Jawaban atas pertanyaan inilah yang menjadi sumbu utama buku ini — sebuah **spektrum** antara *representasi yang dirancang manusia* dan *representasi yang dipelajari mesin*.

Di ujung kiri, *representasi yang dirancang manusia* mencakup segala informasi tambahan yang bentuknya kita tentukan sendiri. Contoh paling sederhana adalah *one-hot encoding* untuk kategori, rasio antara dua kolom, atau *target encoding* yang dihitung dari statistik. Otomasi rekayasa fitur — misalnya algoritma yang mencari kombinasi fitur secara otomatis — juga termasuk di sini, karena bentuk akhir representasi tetap ditentukan oleh aturan dan ruang pencarian yang kita rancang. Mesin hanya menerima fitur yang sudah “matang”; ia tidak menciptakan struktur baru dari data mentah.

Di ujung kanan, *representasi yang dipelajari mesin* tidak dirumuskan secara eksplisit oleh manusia, melainkan dibentuk oleh model selama pelatihan. *Word embedding*, *autoencoder*, dan representasi yang dihasilkan oleh *Graph Neural Network* (GNN) adalah contohnya. Model belajar menemukan sendiri struktur laten yang paling berguna untuk tugas yang dijalani — representasi yang dihasilkan bersifat *implicit* dan tersebar di banyak dimensi.

[GAMBAR 1.1]  
Judul: Spektrum representasi: dari yang dirancang manusia hingga yang dipelajari mesin.  
Tipe: diagram konseptual  
Tampilkan: Sebuah garis horizontal dengan ujung kiri berlabel “dirancang manusia” dan ujung kanan “dipelajari mesin”. Di sepanjang garis, letakkan beberapa contoh teknik pada posisi yang sesuai: di dekat kiri (*one-hot*, *target encoding*, rekayasa fitur otomatis), di tengah (pendekatan hibrida, misalnya *embedding* pra-latih digabung dengan fitur buatan), dan di dekat kanan (*word embedding*, *autoencoder*, GNN). Sumbu horizontal menggambarkan siapa yang menghasilkan representasi: manusia → mesin.

Gambar 1.1 memperlihatkan bahwa dunia representasi bukanlah dua kotak yang terpisah, melainkan sebuah kontinum. Semakin kiri posisi suatu teknik, semakin besar kendali manusia — fitur yang dihasilkan eksplisit, mudah diinterpretasi, dan biasanya memerlukan data yang lebih sedikit. Semakin kanan, semakin besar peran model — representasi yang terbentuk seringkali kaya dan otomatis, tetapi memerlukan data pelatihan dalam jumlah besar dan sulit diurai oleh nalar manusia.

Di tengah spektrum terdapat pendekatan hibrida. Misalnya, kita dapat menggabungkan fitur buatan (seperti statistik pengguna) dengan *embedding* pra-latih dari teks. Model menerima sebagian representasi yang sudah dirancang sekaligus mengambil manfaat dari pengetahuan yang dipelajari mesin secara mandiri — kedua ujung spektrum berdampingan dalam satu model.

Penting dicatat: otomatisasi rekayasa fitur **tidak** otomatis berarti *dipelajari mesin*. Meskipun proses pencariannya otomatis, bentuk akhir fitur tetap ditentukan oleh aturan yang kita tetapkan — bukan oleh model yang belajar dari data mentah. Jadi, otomasi tetap berada di ranah *dirancang manusia*, bukan *dipelajari mesin*.

Setiap kali kita menjumpai teknik baru di buku ini, kita akan bertanya: di manakah posisinya di sepanjang spektrum dirancang–dipelajari? Pertanyaan ini menjadi benang merah yang membantu kita memilih alat yang tepat untuk setiap situasi. Bab berikutnya akan mengupas mitos bahwa “rekayasa fitur sudah mati” — sebuah klaim yang justru mengabaikan peran penting representasi yang dirancang manusia di era *deep learning*.

---

## Sample 6

## Representasi yang Dirancang Manusia vs. Dipelajari Mesin

Sepanjang buku ini, satu pertanyaan akan terus muncul: *siapa yang menentukan bentuk representasi?* Jawabannya membagi pendekatan rekayasa fitur ke dalam dua kutub — dan memahami perbedaan keduanya adalah kunci untuk membaca seluruh buku ini.

Pada kutub pertama, bentuk representasi ditentukan oleh manusia. Kita yang memutuskan bahwa sebuah tanggal perlu dipecah menjadi hari-dalam-minggu, atau bahwa dua kolom harus dibagi untuk menghasilkan rasio. Entah proses itu kita lakukan secara manual baris per baris, atau kita serahkan kepada *pipeline* otomatis yang mencoba ribuan transformasi — selama manusialah yang merancang ruang pencarian dan menetapkan aturan transformasinya, representasi itu tetap *dirancang manusia*. Hasilnya berupa fitur yang eksplisit dan mudah diinterpretasikan: kita tahu persis apa yang diwakili setiap kolom.

Pada kutub kedua, model sendirilah yang membentuk representasi dari data selama pelatihan. Tidak ada manusia yang menentukan "bentuk" fitur itu; model menemukannya sendiri. *Word embedding*, *autoencoder*, dan jaringan berbasis grafis (*GNN*) bekerja dengan cara ini — representasi yang terbentuk bersifat implisit dan tersebar di banyak dimensi, sehingga lebih sulit untuk dibaca secara langsung.

Yang penting, kedua kutub ini bukan dua kotak terpisah, melainkan dua ujung sebuah kontinum. Banyak sistem nyata duduk di tengah: bayangkan model yang menerima *embedding* hasil pralatihan (*pretrained embedding*) sekaligus fitur-fitur hasil rekayasa manual — itulah hibrida yang menggabungkan kekuatan keduanya.

[GAMBAR 1.1]
Judul: Spektrum representasi — dari *dirancang manusia* hingga *dipelajari mesin*
Tipe: diagram konseptual
Tampilkan: Sebuah garis horizontal. Ujung kiri berlabel *dirancang manusia* dengan contoh teknik: *one-hot*, rasio, *target encoding*, automated FE. Ujung kanan berlabel *dipelajari mesin* dengan contoh: *word embedding*, *autoencoder*, GNN. Bagian tengah berlabel *hybrid*. Sumbu horizontal mencerminkan "siapa yang membentuk representasi" — dari manusia ke mesin.

Gambar 1.1 memperlihatkan di mana berbagai teknik jatuh pada spektrum ini. Perhatikan bahwa *one-hot* berada jauh di kiri: manusia yang memutuskan bahwa setiap kategori perlu dikodekan sebagai vektor biner. *Word embedding* berada di kanan karena bentuk representasinya terbentuk seluruhnya dari data teks selama pelatihan. Teknik yang menggabungkan *embedding* pralatihan dengan fitur rekayasa manual mendarat di tengah.

Posisi sebuah teknik pada spektrum ini membawa konsekuensi nyata: semakin ke kanan, semakin besar biaya komputasi dan kebutuhan data, tetapi semakin kecil beban rekayasa manusia. Semakin ke kiri, interpretabilitas cenderung lebih tinggi, dan model sering bekerja baik bahkan dengan data yang terbatas. Tidak ada posisi yang selalu unggul — pilihan bergantung pada konteks, dan mengenali posisi itulah yang akan memandu kita dalam setiap bab berikutnya.

---
