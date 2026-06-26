# Blind Writer Evaluation - ch13_s06: Node embeddings (Node2Vec) 🔢  *(spine pivot + notation + optional figure)*

Score each sample **1-5** on three dimensions (see the rubric):
**D1 Naturalness & correctness . D2 Register & accessibility . D3 Technical & terminological fidelity.**
Please do not try to guess which model wrote which sample.

## Sample 1

**13.6 Node embeddings (Node2Vec)**

Setelah membahas fitur tetangga dan path yang *dirancang manusia* pada subbagian sebelumnya, kita kini memutar poros representasi graf: setiap node akan diwakili oleh vektor padat yang *dipelajari mesin* langsung dari struktur graf. Salah satu metode paling berpengaruh untuk melakukannya adalah Node2Vec.

Node2Vec mengubah graf menjadi kumpulan kalimat dengan cara menjalankan *random walk* berulang dari setiap node. Setiap *walk* menghasilkan urutan node yang diperlakukan sebagai “kata” dalam kalimat. Model *skip-gram*—mirip dengan word2vec—kemudian dilatih untuk memprediksi node-node yang muncul dalam konteks yang sama, sehingga node yang sering bersama dalam *walk* akan memiliki vektor yang mirip.

Node2Vec memberikan dua parameter untuk mengontrol perilaku *walk*: parameter *return* $p$ dan parameter *in-out* $q$. Dengan mengatur $p$ dan $q$, kita dapat menginterpolasi antara eksplorasi BFS (mencerminkan peran struktural) dan DFS (mencerminkan keanggotaan komunitas).

Secara formal, untuk setiap node $u$ kita miliki vektor $\mathbf{z}_u \in \mathbb{R}^{d}$. Tujuan *skip-gram* adalah memaksimalkan likelihood tetangga yang diambil dari *walk*:

$$\max_{f}\ \sum_{u\in V}\log \Pr\!\big(N_S(u)\mid f(u)\big),$$

di mana $f(u)=\mathbf{z}_u$ dan $N_S(u)$ adalah himpunan node yang muncul dalam *walk* di sekitar $u$. Kemiripan antara dua node dihitung dengan *cosine similarity*:

$$\cos(\mathbf{z}_u,\mathbf{z}_v)=\dfrac{\mathbf{z}_u^{\top}\mathbf{z}_v}{\lVert\mathbf{z}_u\rVert\,\lVert\mathbf{z}_v\rVert}.$$

Node yang berdekatan di graf atau yang memiliki peran struktural serupa akan berdekatan pula di ruang vektor.

[GAMBAR 13.6]
Judul: Node dari komunitas yang sama berdekatan dalam ruang embedding
Tipe: diagram konseptual
Tampilkan: Graf kecil dengan beberapa node yang saling berhubungan, dan di sampingnya visualisasi 2D dari vektor embedding yang menunjukkan node-node dari komunitas yang sama berkumpul
Sumber data: –

Gambar 13.6 memperlihatkan bagaimana node-node dari komunitas yang sama di graf menjadi berdekatan dalam ruang embedding, mencerminkan kemiripan peran atau struktur.

Implementasi Node2Vec tersedia di `torch_geometric.nn.Node2Vec` atau paket `node2vec`; parameter utama adalah `dimensions`, `walk_length`, `num_walks`, `p`, dan `q`. Langkah *skip-gram* biasanya menggunakan `gensim` `Word2Vec`. Misalnya, dua pengguna dalam komunitas yang sama akan memiliki vektor yang berdekatan meskipun kita tidak pernah mengekstrak fitur “komunitas” secara manual.

Node2Vec bersifat *transductive*: ia hanya dapat meng-embed node yang ada pada graf pelatihan. Jika kita melatih embedding pada seluruh graf (termasuk node test), kita membocorkan informasi struktur ke test. Oleh karena itu, penggunaan split yang *graph-aware* sangat penting (akan dibahas di s08).

Dengan demikian, representasi yang *dipelajari mesin* ini menggeser beban dari perancang fitur ke algoritma yang memanfaatkan struktur graf secara langsung.

---

## Sample 2

### 13.6 Node Embeddings (Node2Vec)

Pada subbab sebelumnya, kita mengekstrak fitur graf melalui perhitungan yang secara spesifik kita tentukan, seperti derajat node atau jumlah tetangga. Pendekatan tersebut merupakan contoh representasi yang *dirancang manusia*. Sekarang, kita akan melihat pergeseran fundamental menuju representasi yang *dipelajari mesin*. Melalui teknik *node embedding*, setiap node $u$ direpresentasikan sebagai sebuah vektor padat $\mathbf{z}_u \in \mathbb{R}^{d}$. Vektor ini tidak didefinisikan secara manual, melainkan dipelajari langsung dari struktur graf itu sendiri.

Salah satu algoritma paling populer untuk tugas ini adalah Node2Vec. Idenya mengadaptasi konsep *word2vec* dari pemrosesan bahasa alami. Algoritma ini beroperasi dengan menghasilkan sekumpulan *random walk* (lintasan acak) pada graf. Jika kita mengibaratkan graf sebagai sebuah dokumen, maka *random walk* bertindak sebagai "kalimat" dan node yang dilewati adalah "kata". Selanjutnya, sebuah model *skip-gram* dilatih agar node yang berdekatan posisinya dalam sebuah *walk* memiliki vektor yang mirip. Secara matematis, model ini memaksimalkan probabilitas kemunculan tetangga sebuah node pada lintasan tersebut:
$\max_{f}\ \sum_{u\in V}\log \Pr\!\big(N_S(u)\mid f(u)\big)$
Dalam persamaan ini, $f(u)=\mathbf{z}_u$, dan $N_S(u)$ adalah himpunan tetangga node $u$ yang diambil melalui sampel *random walk*.

[GAMBAR 13.1]
Judul: Transformasi graf ke ruang vektor melalui node embedding.
Tipe: diagram konseptual
Tampilkan: Sebuah graf kecil dengan komunitas yang jelas, dipetakan ke ruang embedding 2D di mana node dari komunitas yang sama berada berdekatan.
Sumber data: -

Gambar 13.1 mengilustrasikan hasil dari proses pelatihaan ini. Dua pengguna yang berada dalam satu komunitas yang saling terhubung erat di dalam graf akan mendapatkan vektor yang saling berdekatan di ruang *embedding*, meskipun kita tidak pernah secara eksplisit menghitung fitur "komunitas". Kemiripan atau jarak antarvektor ini umumnya dievaluasi menggunakan *cosine similarity*:
$\cos(\mathbf{z}_u,\mathbf{z}_v)=\dfrac{\mathbf{z}_u^{\top}\mathbf{z}_v}{\lVert\mathbf{z}_u\rVert\,\lVert\mathbf{z}_v\rVert}$

Karakteristik *random walk* dalam Node2Vec dapat disesuaikan menggunakan parameter *return* $p$ dan parameter *in-out* $q$. Kombinasi kedua nilai ini mengatur keseimbangan eksplorasi: apakah *walk* lebih menyerupai *BFS* (fokus pada peran struktural lokal) atau *DFS* (fokus menelusuri kedalaman komunitas). 

Implementasi ini tersedia melalui pustaka `node2vec` atau kelas `torch_geometric.nn.Node2Vec` dengan parameter utama seperti `dimensions`, `walk_length`, `num_walks`, `p`, dan `q`, sementara langkah *skip-gram* di baliknya sering kali mengandalkan `Word2Vec` dari pustaka `gensim`.

Perlu dicatat bahwa metode ini bersifat *transductive*, yang berarti model hanya mempelajari representasi untuk node yang sudah ada di dalam graf saat proses pelatihan. Melatih *embedding* menggunakan graf utuh yang mencakup data uji dapat merusak pemisahan data (kebocoran struktur), sebuah risiko perancangan *pipeline* yang akan kita bahas pada Subbab 13.8. Untuk mengatasi keterbatasan *transductive* ini dan menangani node yang baru muncul, kita akan beralih ke pendekatan induktif pada Subbab 13.7.

---

## Sample 3

## 13.6 Node Embeddings (Node2Vec)

Pada subbab sebelumnya kita membangun fitur-fitur untuk simpul graf secara manual — derajat, agregasi tetangga, atau panjang jalur. Semua itu adalah *representasi yang dirancang manusia*: kita memilih sendiri apa yang ingin diukur dan bagaimana mengukurnya. Kini kita berpindah ke ujung spektrum yang lain. Alih-alih merumuskan fitur, kita meminta model untuk **mempelajari** langsung dari struktur graf — inilah *representasi yang dipelajari mesin* pada ranah graf. Pendekatan yang paling berpengaruh adalah **node embedding** dengan Node2Vec.

Ide dasarnya sederhana dan meminjam keberhasilan *word2vec* di pemrosesan bahasa. Bayangkan kita menelusuri graf secara acak: mulai dari suatu simpul, lalu melangkah ke tetangga, lalu ke tetangganya lagi, terus sepanjang sejumlah langkah tertentu. Deretan simpul yang dikunjungi menjadi semacam “kalimat” — simpul kita anggap sebagai “kata”, dan urutan kunjungan sebagai konteksnya. *Random walk* semacam ini diulang berkali-kali dari setiap simpul, sehingga kita mengumpulkan banyak kalimat buatan. Selanjutnya, kita menerapkan model *skip-gram* yang biasa dipakai di *word2vec*: melatih sebuah vektor padat (*embedding*) untuk setiap simpul agar simpul-simpul yang sering muncul bersama dalam *walk* yang sama memiliki vektor yang mirip. Dengan demikian, relasi struktural yang implisit di graf berubah menjadi kemiripan di ruang vektor.

Agar *walk* tidak sepenuhnya acak dan bisa menekankan aspek struktur yang berbeda, Node2Vec menyediakan dua parameter bias: **return parameter** \(p\) dan **in-out parameter** \(q\). Parameter \(p\) mengontrol seberapa besar peluang *walk* kembali ke simpul sebelumnya, sedangkan \(q\) mengatur kecenderungan *walk* menjauh atau tetap berada di lingkup lokal. Dengan menyetel \(p\) dan \(q\), kita dapat mendorong penjelajahan yang mirip **BFS** (menangkap peran struktural, seperti hub atau jembatan) atau mirip **DFS** (menangkap komunitas). Hasilnya, vektor simpul dapat menonjolkan kemiripan peran ataupun keanggotaan komunitas — tanpa kita perlu merancang metriknya secara eksplisit.

Secara formal, setiap simpul \(u\) kita beri sebuah vektor \(\mathbf{z}_u \in \mathbb{R}^{d}\). Tujuan pelatihan adalah memaksimalkan fungsi objektif *skip-gram* berikut:

\[
\max_{f}\ \sum_{u\in V}\log \Pr\!\big(N_S(u)\mid f(u)\big),
\]

dengan \(f(u) = \mathbf{z}_u\) dan \(N_S(u)\) menyatakan himpunan simpul yang muncul dalam *walk* yang sama dengan \(u\). Dalam praktiknya, probabilitas ini dimodelkan oleh *softmax* sehingga vektor simpul yang berdekatan di *walk* akan semakin mirip. Tingkat kemiripan biasanya diukur dengan **cosine similarity**:

\[
\cos(\mathbf{z}_u,\mathbf{z}_v)=\dfrac{\mathbf{z}_u^{\top}\mathbf{z}_v}{\lVert\mathbf{z}_u\rVert\,\lVert\mathbf{z}_v\rVert}.
\]

[GAMBAR 13.6]
Judul: Pemetaan simpul dari komunitas ke ruang embedding 2D.
Tipe: diagram konseptual.
Tampilkan: sebuah graf kecil dengan dua komunitas rapat, lalu panah menuju ruang vektor 2D di mana simpul-simpul dari komunitas yang sama berkumpul berdekatan.

Gambar 13.6 mengilustrasikan situasi yang umum: dua simpul yang berada dalam komunitas yang sama di graf asli — meskipun tidak kita beri fitur komunitas secara manual — akan otomatis memiliki vektor yang berdekatan di ruang embedding. Kedekatan ini mencerminkan kesamaan peran atau kedekatan struktural yang dipelajari mesin dari pola *walk*.

Perlu dicatat bahwa Node2Vec bersifat **transductive**: embedding yang dihasilkan hanya berlaku untuk simpul-simpul yang ada saat pelatihan. Jika nanti muncul simpul baru, ia tidak langsung memperoleh vektor — berbeda dengan GNN yang induktif (Subbab 13.7). Sifat ini membawa konsekuensi penting pada pipeline: membangun embedding dengan menyertakan seluruh graf, termasuk simpul uji, dapat membocorkan informasi struktur ke tahap pelatihan model hilir. Oleh karena itu, pemisahan data secara sadar-graf (graph-aware split) mutlak diperlukan, seperti yang akan dibahas di Subbab 13.8. Pustaka populer seperti `torch_geometric.nn.Node2Vec` di PyG memudahkan proses menghasilkan *walk* dan melatih *skip-gram*, tetapi pengguna tetap harus waspada terhadap jebakan kebocoran ini.

Dengan Node2Vec, kita telah melangkah dari fitur yang dipilih dan dihitung sendiri menuju representasi vektor yang sepenuhnya dipelajari oleh mesin dari struktur graf. Lompatan ini membuka jalan bagi representasi yang jauh lebih kaya dan adaptif, yang akan kita lanjutkan di subbab berikutnya melalui Graph Neural Networks.

---
