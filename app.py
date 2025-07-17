import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
import json
import time
import os

from rc5_cipher import encrypt_text, decrypt_text

# =======================
# INISIALISASI FLASK APP
# =======================
app = Flask(__name__)

# SECRET KEY WAJIB: GANTI DENGAN YANG KUAT DI PRODUKSI
app.secret_key = 'ini_secret_key_static_ganti_di_produksi' # Contoh: os.urandom(24).hex()

# =======================
# ROUTE: MENU UTAMA
# =======================
@app.route('/')
def menu():
    return render_template('menu.html')

# =======================
# ROUTE: ENKRIPSI + KIRIM EMAIL
# =======================
@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt_page():
    your_email = ''
    app_password = ''
    receiver_email = ''
    subject = ''
    rc5_key = ''
    message_body = ''

    if request.method == 'POST':
        your_email = request.form.get('your_email', '').strip()
        app_password = request.form.get('app_password', '').strip()
        receiver_email = request.form.get('receiver_email', '').strip()
        subject = request.form.get('subject', '').strip()
        rc5_key = request.form.get('rc5_key', '').strip()
        message_body = request.form.get('message_body', '').strip()

        errors = []

        if not your_email:
            errors.append('Email Anda tidak boleh kosong.')
        elif '@' not in your_email:
            errors.append('Format Email Anda tidak valid.')

        if not app_password:
            errors.append('Password aplikasi tidak boleh kosong.')

        if not receiver_email:
            errors.append('Email tujuan tidak boleh kosong.')
        elif '@' not in receiver_email:
            errors.append('Format Email tujuan tidak valid.')

        if not subject:
            errors.append('Subjek email tidak boleh kosong.')

        if not rc5_key:
            errors.append('Kunci RC5 tidak boleh kosong.')

        if not message_body:
            errors.append('Isi pesan tidak boleh kosong.')

        if errors:
            for err in errors:
                flash(err, 'error')
        else:
            try:
                start_time_encrypt = time.perf_counter()
                encrypted_message = encrypt_text(message_body, rc5_key)
                end_time_encrypt = time.perf_counter()
                encryption_duration = end_time_encrypt - start_time_encrypt

                msg = MIMEMultipart()
                msg['From'] = your_email
                msg['To'] = receiver_email
                msg['Subject'] = subject
                msg.attach(MIMEText(encrypted_message, 'plain'))

                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(your_email, app_password)
                    server.sendmail(your_email, receiver_email, msg.as_string())

                flash(f'Email berhasil dikirim!<br>Waktu enkripsi RC5: {encryption_duration:.4f} detik.', 'success')
                return redirect(url_for('encrypt_page'))

            except Exception as e:
                flash(f'Gagal mengirim email: {e}', 'error')

    flashed_messages_list = get_flashed_messages(with_categories=True)
    return render_template('encrypt.html',
                           your_email=your_email,
                           app_password=app_password,
                           receiver_email=receiver_email,
                           subject=subject,
                           rc5_key=rc5_key,
                           message_body=message_body,
                           flashed_messages=flashed_messages_list)

# =======================
# ROUTE: ENKRIPSI SAJA (TANPA KIRIM EMAIL)
# =======================
@app.route('/encrypt_only', methods=['GET', 'POST'])
def encrypt_only_page():
    message_body = ''
    rc5_key = ''
    encrypted_result = None
    
    if request.method == 'POST':
        message_body = request.form.get('message_body', '').strip()
        rc5_key = request.form.get('rc5_key', '').strip()

        errors = []

        if not message_body:
            errors.append('Isi pesan tidak boleh kosong.')
        if not rc5_key:
            errors.append('Kunci RC5 tidak boleh kosong.')

        if errors:
            for err in errors:
                flash(err, 'error')
        else:
            try:
                start_time_encrypt = time.perf_counter()
                encrypted_result = encrypt_text(message_body, rc5_key)
                end_time_encrypt = time.perf_counter()
                encryption_duration = end_time_encrypt - start_time_encrypt
                
                flash(f'Pesan berhasil dienkripsi!<br>Waktu enkripsi RC5: {encryption_duration:.4f} detik.', 'success')

            except Exception as e:
                flash(f'Gagal mengenkripsi: {e}', 'error')
                encrypted_result = f'[Enkripsi gagal: {e}]' # Tampilkan error di area hasil

    flashed_messages_list = get_flashed_messages(with_categories=True)
    return render_template('encrypt_only.html',
                           message_body=message_body,
                           rc5_key=rc5_key,
                           encrypted_result=encrypted_result,
                           flashed_messages=flashed_messages_list)


# =======================
# ROUTE: DEKRIPSI
# =======================
@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt_page():
    decrypted_text_result = None
    ciphertext_b64 = ''
    rc5_key = ''

    if request.method == 'POST':
        ciphertext_b64 = request.form.get('ciphertext', '').strip()
        rc5_key = request.form.get('rc5_key', '').strip()

        has_error = False

        if not ciphertext_b64:
            flash('Ciphertext tidak boleh kosong.', 'error')
            has_error = True

        if not rc5_key:
            flash('Kunci RC5 tidak boleh kosong.', 'error')
            has_error = True

        if not has_error:
            try:
                start_time = time.perf_counter()
                decrypted_text_result = decrypt_text(ciphertext_b64, rc5_key)
                end_time = time.perf_counter()
                decryption_duration = end_time - start_time

                flash(f'Pesan berhasil didekripsi!<br>Waktu dekripsi RC5: {decryption_duration:.4f} detik.', 'success')

            except Exception as e:
                decrypted_text_result = f'[Dekripsi gagal: {e}]'
                flash(f'Gagal mendekripsi: {e}. Pastikan ciphertext dan kunci benar.', 'error')

    flashed_messages_list = get_flashed_messages(with_categories=True)
    return render_template(
        'decrypt.html',
        ciphertext=ciphertext_b64,
        rc5_key=rc5_key,
        decrypted_result=decrypted_text_result,
        flashed_messages=flashed_messages_list
    )

# =======================
# JALANKAN APLIKASI
# =======================
if __name__ == '__main__':
    app.run(debug=True)
