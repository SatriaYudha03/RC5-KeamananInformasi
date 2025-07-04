import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, redirect, url_for, flash
from rc5_cipher import encrypt_text, decrypt_text

app = Flask(__name__)
# Penting: Ganti dengan kunci rahasia yang kuat untuk keamanan sesi dan flash messages
app.secret_key = 'ganti_dengan_kunci_rahasia_yang_sangat_kuat_dan_unik_anda'

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
        app_password = request.form.get('app_password')
        receiver_email = request.form.get('receiver_email')
        subject = request.form.get('subject')
        rc5_key = request.form.get('rc5_key')
        message_body = request.form.get('message_body')

        # Validasi dasar: Kunci RC5 tidak boleh kosong
        if not rc5_key:
            flash('Kunci RC5 tidak boleh kosong!', 'error')
            # Mengembalikan nilai form yang sudah diisi agar pengguna tidak perlu mengetik ulang
            return render_template('encrypt.html',
                                   your_email=your_email,
                                   app_password=app_password,
                                   receiver_email=receiver_email,
                                   subject=subject,
                                   rc5_key=rc5_key,
                                   message_body=message_body)
        try:
            # Memanggil fungsi enkripsi RC5 dari rc5_cipher.py
            encrypted_message = encrypt_text(message_body, rc5_key)

            # Membuat objek email MIME
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
            server.login(your_email, app_password) # Login ke akun email
            server.sendmail(your_email, receiver_email, msg.as_string()) # Mengirim email
            server.quit() # Menutup koneksi SMTP

            flash('Email berhasil dikirim!', 'success')
            # Redirect ke halaman yang sama untuk mencegah pengiriman ulang formulir saat refresh
            return redirect(url_for('encrypt_page'))

        except Exception as e:
            # Menangani error saat pengiriman email atau enkripsi
            flash(f'Gagal mengirim email: {e}', 'error')
            # Mengembalikan nilai form yang sudah diisi jika terjadi error
            return render_template('encrypt.html',
                                   your_email=your_email,
                                   app_password=app_password,
                                   receiver_email=receiver_email,
                                   subject=subject,
                                   rc5_key=rc5_key,
                                   message_body=message_body)
    # Jika request adalah GET, tampilkan formulir enkripsi kosong
    return render_template('encrypt.html')

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
            # Memanggil fungsi dekripsi RC5 dari rc5_cipher.py
            decrypted_text_result = decrypt_text(ciphertext_b64, rc5_key)
            flash('Pesan berhasil didekripsi!', 'success')
        except Exception as e:
            # Menangani error saat dekripsi
            flash(f'Gagal mendekripsi: {e}. Pastikan ciphertext dan kunci benar.', 'error')
            decrypted_text_result = f"Error: {e}" # Menampilkan pesan error di area hasil

        # Menampilkan kembali halaman dekripsi dengan hasil atau pesan error
        return render_template('decrypt.html',
                               ciphertext=ciphertext_b64,
                               rc5_key=rc5_key,
                               decrypted_result=decrypted_text_result)
    # Jika request adalah GET, tampilkan formulir dekripsi kosong
    return render_template('decrypt.html')

# Menjalankan aplikasi Flask jika file ini dieksekusi langsung
if __name__ == '__main__':
    # app.run(debug=True) akan otomatis me-reload server saat ada perubahan kode
    # dan memberikan output debug yang lebih detail di konsol.
    app.run(debug=True)
