# Blind Writer Evaluation - ch06_s06: Date/time and cyclical features  *(technical + required figure + model-family callout)*

Score each sample **1-5** on three dimensions (see the rubric):
**D1 Naturalness & correctness . D2 Register & accessibility . D3 Technical & terminological fidelity.**
Please do not try to guess which model wrote which sample.

## Sample 1

Fitur Tanggal/Waktu dan Fitur Siklik

Kolom datetime mentah menyimpan sekian banyak informasi—jam, hari, bulan, kuartal—yang bisa menjadi sinyal prediktif kuat. Namun, cara kita mengubahnya menjadi *feature* numerik menentukan apakah model benar-benar dapat menangkap maknanya. Menggunakan nilai integer mentah, misalnya jam 0 sampai 23, justru menimbulkan distorsi: bagi model yang peka terhadap jarak, jam 23 terlihat sangat jauh dari jam 0 padahal keduanya berdekatan dalam siklus harian.

Masalah ini muncul karena komponen waktu bersifat siklik, bukan linear. Solusinya adalah *cyclical encoding* yang memetakan nilai periodik ke posisi pada lingkaran satuan menggunakan fungsi sinus dan kosinus. Pemetaan ini memastikan akhir siklus menyambung kembali ke awal, sehingga jam 23 dan jam 00 kembali menjadi tetangga—sesuatu yang tidak bisa dicapai oleh *one-hot* yang membuang informasi ordering sepenuhnya.

Untuk nilai $t$ dengan periode $T$, kita buat dua kolom sekaligus:
$x_{\sin}=\sin\!\big(\tfrac{2\pi t}{T}\big),\qquad x_{\cos}=\cos\!\big(\tfrac{2\pi t}{T}\big)$
Jam dalam sehari menggunakan $T=24$, sedangkan hari dalam minggu menggunakan $T=7$. Pasangan ini menempatkan setiap titik waktu pada koordinat unik di lingkaran, bukan di garis lurus.

[GAMBAR 6.x]
Judul: Encoding siklik pada lingkaran satuan
Tipe: diagram konseptual
Tampilkan: titik jam 0–23 pada lingkaran satuan dengan sumbu $x_{\cos}$ (horizontal) dan $x_{\sin}$ (vertikal), memperlihatkan jam 23 dan jam 0 bersebelahan; di bawahnya garis lurus 0..23 (encoding integer naif) yang justru menempatkan 23 dan 0 berjauhan.
Sumber data: ->

Gambar 6.x mengilustrasikan perbedaan mendasar ini. Bagian atas menampilkan garis integer 0–23 di mana titik ujung terpisah jauh. Bagian bawah menunjukkan lingkaran satuan dengan sumbu $x_{\cos}$ horizontal dan $x_{\sin}$ vertikal, di mana jam 23 dan jam 0 hampir bertumpuk. Perbedaan ini menunjukkan mengapa *encoding* siklik memperbaiki distorsi jarak.

Kedua kolom harus selalu digunakan bersama. Jika hanya sinus atau kosinus saja, jam 6 dan 18—yang berbeda setengah putaran—akan memiliki nilai identik, menimbulkan ambiguitas. Pasangan lengkapnya memastikan setiap waktu memiliki posisi unik di bidang dua dimensi.

Bayangkan memprediksi permintaan layanan transportasi. Pola pada jam 23:00 serupa dengan jam 00:00—keduanya di malam hari dengan volume rendah. *Encoding* integer memaksa model linear menganggapnya sangat berbeda, sementara *encoding* siklik memperbaiki distorsi ini dan memungkinkan model menangkap kontinuitas alami.

Selain *encoding* siklik, kita sering membuat fitur tanggal/waktu lainnya secara eksplisit: *flag* akhir pekan, kategori bulan, jarak ke hari libur, atau waktu sejak event tertentu. Fitur-fitur ini menangkap pengetahuan domain secara langsung dan melengkapi representasi temporal.

Keuntungan *encoding* siklik paling terasa pada model yang mengandalkan geometri jarak, seperti regresi linear, *k*-means, atau *neural network* sederhana. Bagi *tree*—seperti *random forest* atau *gradient boosting*—yang mempartisi berdasarkan *threshold*, manfaatnya biasanya minimal karena pembelahan dapat mengakomodasi pola periodik meski tanpa transformasi.

Transformasi ini *stateless*: parameter $T$ ditetapkan dari domain, bukan dipelajari dari data. Oleh karena itu, tidak ada risiko *leakage* dan aman diterapkan pada *train* dan *test split* tanpa perlu *fitting*. Ini kontras dengan *encoder* yang mempelajari statistik dari data.

Di pandas, aksesor `.dt` memberikan komponen waktu seperti `hour`, `dayofweek`, atau `month`. Untuk *encoding* siklik, kita biasanya menulis fungsi kustom atau menggunakan `FunctionTransformer`; scikit-learn belum menyediakan *encoder* khusus untuk ini. Dengan pemilihan *encoding* yang tepat, fitur temporal menjadi jauh lebih informatif bagi model.

---

## Sample 2

### 6.6 Waktu, Tanggal, dan Fitur Siklik

Data waktu sering kali menyimpan sinyal yang kuat untuk prediksi. Kita dapat dengan mudah mengekstrak komponen kalender dasar seperti `hour`, `dayofweek`, atau `month` dari sebuah *timestamp* menggunakan aksesor `.dt` pada pandas. Selain itu, kita juga dapat merancang fitur tambahan berbasis domain seperti penanda akhir pekan, hari libur, atau waktu yang telah berlalu sejak kejadian tertentu.

Namun, kita akan menghadapi masalah mendasar pada fitur yang nilainya berulang secara periodik, seperti jam dalam sehari atau bulan dalam setahun. Jika kita membiarkan jam sebagai bilangan bulat (0 hingga 23), model akan menganggap jam 23 dan jam 0 berada sangat jauh. Padahal, kedua waktu tersebut bersebelahan secara kronologis. Di sisi lain, mengubahnya menjadi representasi *one-hot* justru akan membuang seluruh informasi tentang urutan dan kedekatan antarwaktu.

Pendekatan yang lebih baik adalah menggunakan *cyclical encoding*, yaitu memetakan nilai siklik ke lingkaran lewat sinus dan kosinus. Untuk sebuah nilai $t$ dengan periode $T$, kita menghitung dua *feature* baru:

$x_{\sin}=\sin\!\big(\tfrac{2\pi t}{T}\big),\qquad x_{\cos}=\cos\!\big(\tfrac{2\pi t}{T}\big)$

Sebagai contoh, fitur jam dalam sehari menggunakan $T=24$, sedangkan hari dalam seminggu menggunakan $T=7$. Kita harus selalu menyertakan kedua kolom ini secara bersamaan. Jika kita hanya menggunakan salah satu, nilainya akan menjadi ambigu karena ada dua waktu berbeda yang dapat menghasilkan nilai sinus atau kosinus yang sama. Pasangan sinus dan kosinus ini bekerja sama untuk menetapkan sebuah titik unik pada lingkaran satuan.

[GAMBAR 6.1]
Judul: Representasi siklik pada lingkaran satuan
Tipe: diagram konseptual
Tampilkan: titik jam 0–23 pada lingkaran satuan dengan sumbu $x_{\cos}$ (horizontal) dan $x_{\sin}$ (vertikal), memperlihatkan jam 23 dan jam 0 bersebelahan; di bawahnya garis lurus 0..23 (encoding integer naif) yang justru menempatkan 23 dan 0 berjauhan.
Sumber data: -

Gambar 6.1 memperlihatkan bagaimana pemetaan melingkar ini memperbaiki kelemahan *encoding* integer naif. Pada garis lurus, ujung awal dan akhir terputus. Namun pada lingkaran satuan, jam 23 melingkar kembali dan bertemu dengan jam 0. Geometri ini sangat krusial, misalnya, ketika kita memprediksi permintaan pelanggan pada larut malam, di mana perilaku pada pukul 23:00 dan 00:00 sangat mirip. Representasi integer akan menyesatkan model linear, sedangkan pasangan siklik mengembalikan kedekatan tersebut.

Dalam praktiknya, scikit-learn tidak memiliki fungsi bawaan khusus untuk *cyclical encoding*. Kita dapat mengimplementasikannya melalui transformasi kustom (misalnya menggunakan `FunctionTransformer`). Transformasi ini murni bersifat *stateless*, artinya tidak ada parameter yang dipelajari dari data pelatihan. Oleh karena itu, langkah ini tidak membawa risiko *leakage* pada *pipeline*.

Penting untuk dicatat bahwa manfaat dari *cyclical encoding* sangat bergantung pada keluarga model yang digunakan. Model linear dan model berbasis jarak sangat membutuhkan representasi geometris ini agar dapat membaca kedekatan waktu dengan benar. Sebaliknya, model berbasis pohon (*tree models*) sering kali tidak memedulikan pemetaan ini dan mampu memilah fitur waktu dalam bentuk integer naif tanpa penurunan performa yang berarti.

---

## Sample 3

### 6.6 Fitur Tanggal/Waktu danEncoding Siklik

Kolom tanggal dan waktu (jam, hari dalam seminggu, bulan) menyimpan sinyal yang kuat untuk banyak persoalan prediksi, tetapi representasi naifnya mudah menyesatkan. Jika jam diperlakukan sebagai bilangan bulat 0–23, jarak antara pukul 23 dan pukul 0 tampak sejauh 23 satuan, padahal keduanya bersebelahan dalam siklus harian. Sementara itu, *one-hot encoding* menghilangkan urutan dan kedekatan sama sekali: setiap jam dianggap sama jauh dari yang lain. Kedua pendekatan ini gagal menangkap sifat periodik data.

*Encoding siklik* (cyclical encoding) memperbaiki masalah tersebut dengan memetakan nilai periodik ke sebuah lingkaran. Untuk suatu nilai $t$ dengan periode $T$, kita menghitung dua kolom baru:

$$
x_{\sin} = \sin\!\Big(\frac{2\pi t}{T}\Big),\qquad
x_{\cos} = \cos\!\Big(\frac{2\pi t}{T}\Big).
$$

Pasangan sinus dan kosinus ini menempatkan setiap nilai $t$ sebagai satu titik pada lingkaran satuan. Misalnya, jam dalam sehari menggunakan $T=24$; titik untuk pukul 23 dan pukul 0 akan berdekatan di lingkaran, sehingga model linear yang membaca geometri ruang fitur tidak lagi “melihat” keduanya sebagai nilai yang berjauhan. Kedua kolom **harus hadir bersama**: sinus saja tidak cukup karena dua jam yang berbeda dapat menghasilkan nilai sinus yang sama (misalnya $\sin(\pi/6) = \sin(5\pi/6)$), sedangkan kosinus membedakannya. Hanya dengan pasangan $(x_{\sin}, x_{\cos})$ kita memperoleh posisi unik pada lingkaran.

[GAMBAR 6.x]  
Judul: Encoding siklik pada lingkaran satuan.  
Tipe: diagram konseptual.  
Tampilkan: titik-titik jam 0 hingga 23 pada lingkaran satuan dengan sumbu horizontal $x_{\cos}$ dan sumbu vertikal $x_{\sin}$, memperlihatkan bahwa jam 23 dan jam 0 bersebelahan; di bawahnya, garis lurus 0..23 (encoding integer naif) yang justru menempatkan 23 dan 0 berjauhan.

Gambar 6.x memperlihatkan perbandingan kedua pendekatan secara visual. Lingkaran satuan di bagian atas menunjukkan bagaimana *encoding* siklik “membungkus” ujung siklus sehingga nilai yang berdekatan secara temporal tetap berdekatan dalam ruang fitur. Garis lurus di bawahnya menggambarkan kelemahan representasi integer: pukul 23 dan 0 terpisah jauh, padahal secara perilaku keduanya sering mirip—misalnya dalam prediksi permintaan layanan, pukul 23:00 dan 00:00 sama-sama menunjukkan aktivitas rendah.

Fitur tanggal/waktu lain tetap kita bangun secara eksplisit sebagai fitur yang *dirancang manusia*: hari dalam seminggu, flag akhir pekan (*is_weekend*), bulan, penanda hari libur, atau selisih waktu sejak suatu kejadian (*time-since-event*). Semua ini menyuntikkan pengetahuan domain ke dalam data tanpa perlu dipelajari oleh model. *Encoding* siklik sendiri dapat dihitung dengan aksesor `.dt` di pandas (misalnya `df['jam'].dt.hour`) lalu diolah melalui transformer kustom seperti `FunctionTransformer`. Perlu dicatat bahwa scikit-learn tidak menyediakan *cyclical encoder* khusus; kita cukup menulis fungsi pendek yang menghitung pasangan sinus/kosinus.

Dari sisi disiplin *pipeline*, transformasi ini sepenuhnya *stateless*—tidak ada parameter yang diestimasi dari data—sehingga tidak menimbulkan risiko kebocoran (*leakage*). Ini menjadi kontras yang berguna dengan *encoder* atau *scaler* yang harus di-*fit* pada data latih.

Secara praktis, *encoding* siklik paling membantu model berbasis jarak dan model linear yang memanfaatkan geometri fitur. Model pohon (*tree-based*) sering kali tidak memerlukannya karena mereka dapat mempartisi ruang berdasarkan ambang tertentu; namun, jika interaksi antarwaktu penting, pasangan siklik ini tetap bisa memberi manfaat. Subbab berikutnya akan membahas ledakan fitur (*feature explosion*) yang dapat muncul ketika kita mengkombinasikan banyak fitur turunan, dan Bab 10 akan memperluas bahasan ke fitur temporal yang lebih kompleks seperti jendela waktu (*window*).

---
