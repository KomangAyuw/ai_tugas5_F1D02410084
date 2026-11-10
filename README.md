# Tugas 5
# KarirKu: Sistem Pakar Rekomendasi Bidang Karier Berdasarkan Minat dan Kemampuan Menggunakan Metode Forward Chaining
- Nama : NI KOMANG AYU SUMEITRI
- NIM  : F1D02410084
- Mata kuliah: Kecerdasan Buatan

## 2. Topik dan cara menjalankan

**Topik:** rekomendasi bidang karier untuk masyarakat umum (pelajar, mahasiswa, pencari kerja, maupun pekerja yang ingin berganti jalur), berdasarkan **minat** dan **kemampuan**. Minat dikelompokkan dengan teori RIASEC Holland (Realistic, Investigative, Artistic, Social, Enterprising, Conventional), sedangkan kemampuan dinilai dari keterampilan kerja yang didefinisikan O*NET. Sistem ini menggunakan metode **Forward Chaining**, yaitu metode penalaran maju yang dimulai dari fakta-fakta yang diketahui (jawaban pengguna), kemudian mencocokkannya dengan aturan IF-THEN dalam basis pengetahuan untuk menghasilkan fakta baru, dan proses ini diulang terus sampai tidak ada aturan baru yang bisa dijalankan sehingga diperoleh kesimpulan akhir.

**Bahasa:** Python 3 (dicoba pada Python 3.13).

**File:**

| File | Isi |
|---|---|
| `kb_karier.json` | basis aturan: 36 aturan IF-THEN, 30 pernyataan yang ditanyakan, 5 sumber |

## 3. Sumber dan tabel aturan

### Sumber

| Kode | Sumber |
|---|---|
| S1 | O*NET OnLine. (n.d.). *Browse by Career Interest Types (1.B.1)*. U.S. Department of Labor, Employment and Training Administration. https://www.onetonline.org/find/descriptor/browse/1.B.1. Diakses 10 November 2026. |
| S2 | O*NET OnLine. (n.d.). *Browse by Transferable Skills (2.B)*. U.S. Department of Labor, Employment and Training Administration. https://www.onetonline.org/find/descriptor/browse/2.B. Diakses 10 November 2026. |
| S3 | O*NET OnLine. (n.d.). *Browse by Essential Skills (2.A)*. U.S. Department of Labor, Employment and Training Administration. https://www.onetonline.org/find/descriptor/browse/2.A. Diakses 10 November 2026. |
| S4 | Rianto, V. Y., & Wulandari, S. (2025). Aplikasi Tes Minat Bakat dan Perencanaan Karier Menggunakan Adaptasi Teori RIASEC Berbasis Forward Chaining. *TIN: Terapan Informatika Nusantara*, 6(7), 1092–1104. https://doi.org/10.47065/tin.v6i7.8544. Diakses 10 November 2026. |
| S5 | Fatmasari, & Supriyatna, A. (2019). Pemilihan dan Pengembangan Karier Berdasarkan Minat, Bakat dan Kepribadian Remaja Menggunakan Forward Chaining. *JUITA*, VII(1), 33–42. p-ISSN 2086-9398, e-ISSN 2579-9801. https://www.researchgate.net/publication/333899668_Pemilihan_dan_Pengembangan_Karier_Berdasarkan_Minat_Bakat_dan_Kepribadian_Remaja_Menggunakan_Forward_Chaining. Diakses 10 November 2026. |

S1 sampai S3 adalah situs resmi pemerintah Amerika Serikat (lisensi CC BY 4.0). S4 dan S5 adalah jurnal ilmiah. Aturan ditulis dengan kalimat sendiri (parafrasa), bukan kutipan.

### Dari mana aturan berasal

- **Enam tipe minat dan bidang pekerjaan yang terkait** diambil dari definisi O*NET (S1), misalnya tipe Realistic berkaitan dengan merancang, membangun, atau memperbaiki peralatan, bekerja di luar ruangan, dan kegiatan fisik.
- **Pernyataan minat** (18 butir) diturunkan dari definisi tipe pada S1 dan dicocokkan dengan butir pertanyaan pada dua jurnal (S4, S5). S4 memakai kategori Teknik, Sains, Kesenian, Wirausaha, Pendidikan, Kesehatan. S5 memakai enam tipe Holland lengkap termasuk Conventional, karena itu tipe Conventional bersumber pada S1 dan S5.
- **Pernyataan kemampuan** (12 butir) diturunkan dari daftar keterampilan O*NET: *Repairing*, *Troubleshooting*, *Science*, *Mathematics*, *Writing*, *Instructing*, *Active Listening*, *Persuasion*, *Negotiation*, *Management of Financial Resources*, *Reading Comprehension* (S2, S3).

### Tabel aturan (36 aturan)

Fakta dasar yang ditanyakan ke pengguna memakai awalan `i_` (minat) dan `k_` (kemampuan). Huruf berikutnya adalah tipe Holland (r, i, a, s, e, c).

**Lapis 1: fakta minat menjadi minat tipe tertentu.** Dua dari tiga pernyataan minat pada satu tipe sudah cukup, sehingga tiap tipe punya tiga aturan.

| Aturan | IF | THEN | Sumber |
|---|---|---|---|
| R01 | `i_r1` DAN `i_r2` | `minat_realistic` | S1, S4, S5 |
| R02 | `i_r1` DAN `i_r3` | `minat_realistic` | S1, S4, S5 |
| R03 | `i_r2` DAN `i_r3` | `minat_realistic` | S1, S4, S5 |
| R04 – R06 | pasangan `i_i1`, `i_i2`, `i_i3` (DAN) | `minat_investigative` | S1, S4, S5 |
| R07 – R09 | pasangan `i_a1`, `i_a2`, `i_a3` (DAN) | `minat_artistic` | S1, S4, S5 |
| R10 – R12 | pasangan `i_s1`, `i_s2`, `i_s3` (DAN) | `minat_social` | S1, S4, S5 |
| R13 – R15 | pasangan `i_e1`, `i_e2`, `i_e3` (DAN) | `minat_enterprising` | S1, S4, S5 |
| R16 – R18 | pasangan `i_c1`, `i_c2`, `i_c3` (DAN) | `minat_conventional` | S1, S5 |

**Lapis 2: fakta kemampuan menjadi kemampuan pendukung.** Satu dari dua pernyataan kemampuan sudah cukup (mode ATAU), supaya sistem tidak terlalu kaku.

| Aturan | IF | THEN | Sumber |
|---|---|---|---|
| R19 | `k_r1` ATAU `k_r2` (memperbaiki, menelusuri penyebab masalah alat) | `kemampuan_realistic` | S2 |
| R20 | `k_i1` ATAU `k_i2` (metode ilmiah, matematika) | `kemampuan_investigative` | S3 |
| R21 | `k_a1` ATAU `k_a2` (menulis, atau berkarya visual/musik) | `kemampuan_artistic` | S1, S3 |
| R22 | `k_s1` ATAU `k_s2` (mengajar, mendengarkan aktif) | `kemampuan_social` | S2, S3 |
| R23 | `k_e1` ATAU `k_e2` (membujuk, bernegosiasi) | `kemampuan_enterprising` | S2 |
| R24 | `k_c1` ATAU `k_c2` (mengelola anggaran, memahami prosedur tertulis) | `kemampuan_conventional` | S2, S3 |

**Lapis 3: minat dan kemampuan menjadi kesimpulan "cocok".** Aturan ini memakai hasil aturan lapis 1 dan 2, sehingga rantai inferensinya tiga tingkat.

| Aturan | IF | THEN (kesimpulan) | Sumber |
|---|---|---|---|
| R25 | `minat_realistic` DAN `kemampuan_realistic` | `karier_realistic`: Teknik, Mekanik, dan Pekerjaan Lapangan | S1 |
| R26 | `minat_investigative` DAN `kemampuan_investigative` | `karier_investigative`: Sains, Penelitian, dan Teknologi Informasi | S1 |
| R27 | `minat_artistic` DAN `kemampuan_artistic` | `karier_artistic`: Seni, Desain, dan Media Kreatif | S1 |
| R28 | `minat_social` DAN `kemampuan_social` | `karier_social`: Pendidikan dan Layanan Sosial | S1 |
| R29 | `minat_enterprising` DAN `kemampuan_enterprising` | `karier_enterprising`: Bisnis, Manajemen, dan Kepemimpinan | S1 |
| R30 | `minat_conventional` DAN `kemampuan_conventional` | `karier_conventional`: Administrasi, Data, dan Keuangan | S1 |

**Lapis 4: minat saja menjadi kesimpulan "arah eksplorasi".** Bila minat tipe tertentu terpenuhi tetapi kemampuan belum terlihat, sistem tetap memberi arah awal dan tidak mengembalikan hasil kosong.

| Aturan | IF | THEN | Sumber |
|---|---|---|---|
| R31 – R36 | `minat_realistic` / `minat_investigative` / `minat_artistic` / `minat_social` / `minat_enterprising` / `minat_conventional` | `eksplorasi_realistic` / `eksplorasi_investigative` / `eksplorasi_artistic` / `eksplorasi_social` / `eksplorasi_enterprising` / `eksplorasi_conventional` | S1 |

Jika kesimpulan "cocok" untuk suatu tipe sudah ada, kesimpulan "arah eksplorasi" untuk tipe yang sama tidak ditampilkan lagi (diatur lewat kolom `diganti_oleh` di file aturan).

Ada 12 kesimpulan (6 tipe, masing-masing tingkat "cocok" dan "arah eksplorasi"); syarat minimal adalah 3. Bidang pekerjaan yang ditampilkan adalah terjemahan bebas dari daftar bidang terkait pada S1.

## 4. Metode yang dipilih dan alasannya

**Metode: Forward Chaining (FC).** Forward chaining adalah metode penalaran maju (data-driven) pada sistem pakar. Penalaran dimulai dari fakta yang diketahui, lalu aturan IF-THEN yang syaratnya terpenuhi dijalankan untuk menambah fakta baru, dan proses diulang sampai tidak ada aturan baru yang bisa dijalankan.

**Alasan memilih FC:**

1. Masukan sistem berupa fakta jawaban pengguna (minat dan kemampuan), sedangkan kesimpulannya belum ditentukan sebelumnya. Penalaran yang bergerak dari fakta menuju kesimpulan sesuai dengan sifat masalah ini.
2. Satu orang bisa memiliki beberapa bidang karier yang cocok sekaligus. FC otomatis menemukan semua kesimpulan yang mungkin, sedangkan Backward Chaining (BC) harus memilih satu tujuan lebih dulu lalu menelusurinya satu per satu.
3. Dua jurnal acuan (S4 dan S5) juga memakai FC untuk kasus rekomendasi karier serupa.
4. Aturan bersifat berantai (jawaban → minat dan kemampuan → bidang karier), sehingga cocok dijalankan secara bertahap oleh FC.

## 5. Kasus uji dan screenshot

## 6. Batas keberlakuan

Pengetahuan dalam sistem ini berasal dari basis data O*NET OnLine milik Departemen Tenaga Kerja Amerika Serikat, sehingga mengikuti konteks pasar kerja Amerika, serta dari dua jurnal sistem pakar karier di Indonesia (2019 dan 2025). Sistem hanya memetakan enam rumpun minat Holland dan enam kelompok kemampuan dari jawaban ya atau tidak. Hasil "arah eksplorasi" hanya berdasarkan minat. Hasilnya cocok sebagai saran awal bagi masyarakat umum untuk mengeksplorasi pilihan karier, bukan keputusan akhir, dan tidak menggantikan konseling karier atau tes psikologi baku. Sistem tidak mempertimbangkan jenjang pendidikan, kondisi ekonomi, minat yang berubah, maupun kebutuhan pasar kerja Indonesia. Catatan yang sama ditampilkan di akhir keluaran program.

## 7. Penggunaan alat bantu AI
- Saya memakai Chatgpt untuk brainstorming mencari topik dan juga membantu mencari jurnal referensi.