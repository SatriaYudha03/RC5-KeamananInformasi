import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
import json # Import modul json
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
        your_email = request.form.get('your_email')
        receiver_email = request.form.get('receiver_email')
        subject = request.form.get('subject')
        rc5_key = request.form.get('rc5_key')
        message_body = request.form.get('message_body')

        if not rc5_key:
            flash('Kunci RC5 tidak boleh kosong!', 'error')
            return render_template('encrypt.html',
                                   your_email=your_email,
                                   receiver_email=receiver_email,
                                   subject=subject,
                                   rc5_key=rc5_key,
                                   message_body=message_body)
        try:
            encrypted_message = encrypt_text(message_body, rc5_key)

            msg = MIMEMultipart()
            msg['From'] = your_email
            msg['To'] = receiver_email
            msg['Subject'] = subject
            msg.attach(MIMEText(encrypted_message, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(your_email, GMAIL_APP_PASSWORD)
            server.sendmail(your_email, receiver_email, msg.as_string())
            server.quit()

            flash('Email berhasil dikirim!', 'success')
            return redirect(url_for('encrypt_page'))

        except Exception as e:
            flash(f'Gagal mengirim email: {e}', 'error')
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
    decrypted_text_result = None
    if request.method == 'POST':
        ciphertext_b64 = request.form.get('ciphertext')
        rc5_key = request.form.get('rc5_key')

        if not rc5_key:
            flash('Kunci RC5 tidak boleh kosong!', 'error')
            return render_template('decrypt.html',
                                   ciphertext=ciphertext_b64,
                                   rc5_key=rc5_key)

        try:
            decrypted_text_result = decrypt_text(ciphertext_b64, rc5_key)
            flash('Pesan berhasil didekripsi!', 'success')
        except Exception as e:
            flash(f'Gagal mendekripsi: {e}. Pastikan ciphertext dan kunci benar.', 'error')
            decrypted_text_result = f"Error: {e}"

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
    app.run(debug=True)
