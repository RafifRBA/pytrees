# Belajar dan Memahami Code untuk Selector, Sequence, dan Parallel

### 1. Selector
Selector mengevaluasi anak-anaknya (*children*) dari **kiri ke kanan**. 
* Pada satu kali tick, jika anak me-return **FAILURE**, ia akan lanjut mengecek anak berikutnya.
* Jika anak me-return **SUCCESS** atau **RUNNING**, proses pengecekan langsung berhenti di anak tersebut dan Selector akan ikut me-return status yang sama. 
* *Fungsi Utama:* Biasanya digunakan untuk penanganan **prioritas** atau *fallback* (misal: Node kiri untuk deteksi bahaya pencegah tabrakan, Node kanan untuk aktivitas jalan normal).

### 2. Sequence
Sequence juga mengevaluasi anak-anaknya dari **kiri ke kanan**, tetapi dengan aturan kebalikan dari Selector.
* Pada satu kali tick, jika anak me-return **SUCCESS**, ia akan langsung lanjut mengecek dan mengeksekusi anak berikutnya di tick yang sama.
* Jika anak me-return **RUNNING** atau **FAILURE**, proses pengecekan berhenti di situ.
* *Fungsi Utama:* Digunakan untuk mengeksekusi **daftar tugas berurutan** (*checklist*). Sangat sering diatur dengan `memory=True` agar ia mengingat sejauh mana langkah tugas yang sudah berhasil dikerjakan, sehingga tidak mengulang dari awal pada tick berikutnya.

### 3. Parallel
Parallel men-`tick` **seluruh anaknya secara serentak** dalam satu siklus tick secara konseptual.
* Secara umum ia akan me-return **FAILURE** jika ada satu saja anaknya yang gagal (*FAILURE*).
* Untuk menentukan kapan ia me-return **SUCCESS**, Parallel mengandalkan sebuah kebijakan (**Policy**), antara lain:
  * `SuccessOnAll`: Baru dianggap berjalan sukses jika *semua* pasukan/anaknya melaporkan SUCCESS.
  * `SuccessOnOne`: Dianggap sukses jika *ada minimal satu* anak yang melaporkan SUCCESS (jika ini terjadi, anak-anak lain yang masih berstatus RUNNING akan dihentikan paksa / diinterupsi).
  * `SuccessOnSelected`: Dianggap sukses bila list subset/anak khusus yang ditentukan berhasil SUCCESS.
* *Fungsi Utama:* Digunakan untuk menjalankan tugas sekunder di latar belakang yang harus ada selama misi utama berlangsung (misalnya: *Context Switch* untuk menghidupkan alarm saat urutan misi utama sedang dijalankan).