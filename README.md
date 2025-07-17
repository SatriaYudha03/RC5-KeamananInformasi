# RC5 Email Encryption System
 Email password app: hwhe netp vzot eqcf
 
## Deskripsi Proyek
Proyek ini adalah implementasi sistem pengiriman pesan email yang aman menggunakan algoritma enkripsi RC5. Aplikasi ini dilengkapi dengan antarmuka web yang modern dan interaktif, memungkinkan pengguna untuk mengenkripsi dan mendekripsi pesan sebelum mengirimkannya melalui email.

**Fitur Utama:**
* **Enkripsi & Dekripsi RC5:** Menggunakan algoritma RC5 untuk mengamankan komunikasi.
* **Antarmuka Web Interaktif:** Dilengkapi dengan halaman menu, enkripsi, dan dekripsi yang intuitif.
* **Animasi Dinamis:** Judul dengan efek cahaya bergelombang dan teks deskripsi dengan animasi mengetik/menghapus.
* **Notifikasi SweetAlert:** Memberikan umpan balik yang modern dan informatif setelah operasi enkripsi/dekripsi.
* **Pengukuran Waktu RC5:** Menampilkan durasi proses enkripsi dan dekripsi RC5.
* **Autofill Styling:** Penanganan gaya input autofill browser agar konsisten dengan tema gelap.

## Instalasi

Untuk menjalankan aplikasi ini di lingkungan lokal Anda, ikuti langkah-langkah berikut:

1.  **Pastikan Python Terinstal:**
    Jika Anda belum memiliki Python, unduh dan instal dari [python.org](https://www.python.org/).

2.  **Buat Lingkungan Virtual (Direkomendasikan):**
    Ini adalah praktik terbaik untuk mengelola dependensi proyek Anda.
    ```bash
    python -m venv venv
    ```

3.  **Aktifkan Lingkungan Virtual:**
    * **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Instal Dependensi Flask:**
    ```bash
    pip install Flask
    ```

5.  **Struktur Proyek:**
    Pastikan struktur folder proyek Anda diatur dengan benar:
    ```
    nama_proyek_anda/
    ├── app.py
    ├── rc5_cipher.py
    ├── templates/
    │   ├── menu.html
    │   ├── encrypt.html
    │   └── decrypt.html
    └── static/
        ├── images/
        │   └── bgKeamanan.png 
        └── script.js           
        └── style.css           
    ```
    * Pastikan semua file Python, HTML, dan JavaScript berada di lokasi yang benar sesuai struktur di atas.

## Cara Menjalankan Aplikasi

Setelah semua dependensi terinstal dan struktur proyek benar, Anda dapat menjalankan aplikasi:

1.  **Navigasi ke Direktori Proyek:**
    Buka terminal atau Command Prompt dan navigasikan ke folder `nama_proyek_anda/` (tempat `app.py` berada).

2.  **Jalankan Aplikasi Flask:**
    ```bash
    python app.py
    ```

3.  **Akses Aplikasi:**
    Buka browser web Anda dan kunjungi URL berikut:
    ```
    [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
    ```

## Detail Email Pengirim

Aplikasi ini dikonfigurasi untuk menggunakan email pengirim tertentu. Anda tidak perlu menginput password aplikasi di antarmuka karena sudah tertanam dalam kode (untuk tujuan demonstrasi/proyek).

**Email Pengirim yang Digunakan:**
`keamananinformasitugas@gmail.com`

**Penting:** Jika Anda menggunakan Gmail, pastikan Anda telah mengaktifkan [Verifikasi 2 Langkah](https://support.google.com/accounts/answer/185834) dan membuat [Password Aplikasi](https://support.google.com/accounts/answer/185834?hl=id#apppasswords) untuk akun ini. Password Aplikasi inilah yang harus Anda masukkan di dalam `app.py` pada variabel `GMAIL_APP_PASSWORD`.

## Kolaborasi Proyek

Projek ini merupakan hasil kolaborasi dari:
* Dwiki (2305551001)
* Satria (2305551058)
* Rifki (2305551068)
* Devasya (2305551074)
* Septino (2305551083)
* Tara (2305551139)