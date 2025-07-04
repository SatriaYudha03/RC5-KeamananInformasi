import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
import json
import time # Import modul time untuk mengukur waktu

# Import fungsi RC5 dari file rc5_cipher.py
from rc5_cipher import encrypt_text, decrypt_text

# ====================================================================
# ===== PENTING: PASSWORD APLIKASI DI-HARDCODE (PERINGATAN KEAMANAN!) =====
# ====================================================================
# Ini adalah password aplikasi Gmail yang Anda berikan.
# INGAT: Menanamkan password langsung di kode sumber tidak disarankan untuk aplikasi produksi.
# Untuk aplikasi riil, gunakan variabel lingkungan atau sistem manajemen rahasia.
GMAIL_APP_PASSWORD = 'hwhe netp vzot eqcf'
# ====================================================================

app = Flask(__name__)
app.secret_key = 'ganti_dengan_kunci_rahasia_yang_sangat_kuat_dan_unik_anda' # Ganti ini!

# --- Rute Halaman Menu ---
@app.route('/')
def menu():
    """
    Menampilkan halaman menu utama aplikasi.
    Pengguna dapat memilih antara mode enkripsi atau dekripsi.
    """
    return render_template('menu.html')

# --- Rute Halaman Enkripsi & Kirim Email ---
@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt_page():
    """
    Menangani tampilan formulir enkripsi (GET request)
    dan pemrosesan data formulir serta pengiriman email terenkripsi (POST request).
    """
    if request.method == 'POST':
        # Mengambil data dari formulir POST
        your_email = request.form.get('your_email')
        receiver_email = request.form.get('receiver_email')
        subject = request.form.get('subject')
        rc5_key = request.form.get('rc5_key')
        message_body = request.form.get('message_body')

        # Validasi dasar: Kunci RC5 tidak boleh kosong
        if not rc5_key:
            flash('Kunci RC5 tidak boleh kosong!', 'error')
            # Mengembalikan nilai form yang sudah diisi
            return render_template('encrypt.html',
                                   your_email=your_email,
                                   receiver_email=receiver_email,
                                   subject=subject,
                                   rc5_key=rc5_key,
                                   message_body=message_body)
        try:
            # --- Mengukur waktu enkripsi RC5 ---
            start_time_encrypt = time.perf_counter()
            encrypted_message = encrypt_text(message_body, rc5_key)
            end_time_encrypt = time.perf_counter()
            encryption_duration = end_time_encrypt - start_time_encrypt
            # -----------------------------------

            msg = MIMEMultipart()
            msg['From'] = your_email
            msg['To'] = receiver_email
            msg['Subject'] = subject
            # Melampirkan pesan terenkripsi sebagai teks biasa
            msg.attach(MIMEText(encrypted_message, 'plain'))

            # Mengatur koneksi SMTP untuk mengirim email
            # Menggunakan port 587 dengan STARTTLS untuk koneksi aman
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls() # Mengamankan koneksi dengan TLS
            server.login(your_email, GMAIL_APP_PASSWORD) # Login ke akun email
            server.sendmail(your_email, receiver_email, msg.as_string()) # Mengirim email
            server.quit() # Menutup koneksi SMTP

            # Menggunakan flash message yang akan ditangkap oleh SweetAlert
            flash(f'Email berhasil dikirim!\nWaktu enkripsi RC5: {encryption_duration:.4f} detik.', 'success')
            # Redirect ke halaman yang sama untuk mencegah pengiriman ulang formulir saat refresh
            return redirect(url_for('encrypt_page'))

        except Exception as e:
            # Menangani error saat pengiriman email atau enkripsi
            # Menggunakan flash message yang akan ditangkap oleh SweetAlert
            flash(f'Gagal mengirim email: {e}', 'error')
            # Mengembalikan nilai form yang sudah diisi jika terjadi error
            return render_template('encrypt.html',
                                   your_email=your_email,
                                   receiver_email=receiver_email,
                                   subject=subject,
                                   rc5_key=rc5_key,
                                   message_body=message_body)
    
    # Ambil flash messages dan konversi ke JSON untuk JavaScript
    flashed_messages = json.dumps(get_flashed_messages(with_categories=True))
    return render_template('encrypt.html', flashed_messages=flashed_messages)

# --- Rute Halaman Dekripsi Pesan ---
@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt_page():
    """
    Menangani tampilan formulir dekripsi (GET request)
    dan pemrosesan data formulir untuk dekripsi (POST request).
    """
    decrypted_text_result = None # Variabel untuk menyimpan hasil dekripsi
    if request.method == 'POST':
        # Mengambil data dari formulir POST
        ciphertext_b64 = request.form.get('ciphertext')
        rc5_key = request.form.get('rc5_key')

        # Validasi dasar: Kunci RC5 tidak boleh kosong
        if not rc5_key:
            flash('Kunci RC5 tidak boleh kosong!', 'error')
            # Mengembalikan nilai form yang sudah diisi
            return render_template('decrypt.html',
                                   ciphertext=ciphertext_b64,
                                   rc5_key=rc5_key)

        try:
            # --- Mengukur waktu dekripsi RC5 ---
            start_time_decrypt = time.perf_counter()
            decrypted_text_result = decrypt_text(ciphertext_b64, rc5_key)
            end_time_decrypt = time.perf_counter()
            decryption_duration = end_time_decrypt - start_time_decrypt
            # -----------------------------------

            # Menggunakan flash message yang akan ditangkap oleh SweetAlert
            flash(f'Pesan berhasil didekripsi!\nWaktu dekripsi RC5: {decryption_duration:.4f} detik.', 'success')
        except Exception as e:
            # Menangani error saat dekripsi
            # Menggunakan flash message yang akan ditangkap oleh SweetAlert
            flash(f'Gagal mendekripsi: {e}. Pastikan ciphertext dan kunci benar.', 'error')
            decrypted_text_result = f"Error: {e}" # Menampilkan pesan error di area hasil

        # Ambil flash messages dan konversi ke JSON untuk JavaScript
        flashed_messages = json.dumps(get_flashed_messages(with_categories=True))
        return render_template('decrypt.html',
                               ciphertext=ciphertext_b64,
                               rc5_key=rc5_key,
                               decrypted_result=decrypted_text_result,
                               flashed_messages=flashed_messages)
    
    # Ambil flash messages dan konversi ke JSON untuk JavaScript
    flashed_messages = json.dumps(get_flashed_messages(with_categories=True))
    return render_template('decrypt.html', flashed_messages=flashed_messages)

if __name__ == '__main__':
    # app.run(debug=True) akan otomatis me-reload server saat ada perubahan kode
    # dan memberikan output debug yang lebih detail di konsol.
    app.run(debug=True)
