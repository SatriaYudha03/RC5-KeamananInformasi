import base64
import smtplib
from tkinter import *
from tkinter import messagebox
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ========== RC5 ALGORITHM ==========
WORD_SIZE = 32
ROUNDS = 12
P = 0xB7E15163
Q = 0x9E3779B9

def rotate_left(val, shift):
    return ((val << shift) & 0xFFFFFFFF) | (val >> (32 - shift))

def rotate_right(val, shift):
    return (val >> shift) | ((val << (32 - shift)) & 0xFFFFFFFF)

def rc5_key_schedule(key, w=32, r=12):
    b = len(key)
    u = w // 8
    c = (b + u - 1) // u
    L = [0] * c
    for i in range(b):
        L[i // u] = (L[i // u] << 8) + key[i]
    t = 2 * (r + 1)
    S = [0] * t
    S[0] = P
    for i in range(1, t):
        S[i] = (S[i - 1] + Q) & 0xFFFFFFFF
    A = B = i = j = 0
    for _ in range(3 * max(t, c)):
        A = S[i] = rotate_left((S[i] + A + B) & 0xFFFFFFFF, 3)
        B = L[j] = rotate_left((L[j] + A + B) & 0xFFFFFFFF, (A + B) % 32)
        i = (i + 1) % t
        j = (j + 1) % c
    return S

def rc5_encrypt(plain_block, S):
    A = int.from_bytes(plain_block[:4], byteorder='little')
    B = int.from_bytes(plain_block[4:], byteorder='little')
    A = (A + S[0]) & 0xFFFFFFFF
    B = (B + S[1]) & 0xFFFFFFFF
    for i in range(1, ROUNDS + 1):
        A = (rotate_left((A ^ B), B % 32) + S[2 * i]) & 0xFFFFFFFF
        B = (rotate_left((B ^ A), A % 32) + S[2 * i + 1]) & 0xFFFFFFFF
    return A.to_bytes(4, byteorder='little') + B.to_bytes(4, byteorder='little')

def rc5_decrypt(cipher_block, S):
    A = int.from_bytes(cipher_block[:4], byteorder='little')
    B = int.from_bytes(cipher_block[4:], byteorder='little')
    for i in range(ROUNDS, 0, -1):
        B = rotate_right((B - S[2 * i + 1]) & 0xFFFFFFFF, A % 32) ^ A
        A = rotate_right((A - S[2 * i]) & 0xFFFFFFFF, B % 32) ^ B
    A = (A - S[0]) & 0xFFFFFFFF
    B = (B - S[1]) & 0xFFFFFFFF
    return A.to_bytes(4, byteorder='little') + B.to_bytes(4, byteorder='little')

def pad_data(data):
    while len(data) % 8 != 0:
        data += b'\x00'
    return data

def encrypt_text(plaintext, key):
    key_bytes = key.encode('utf-8')
    data = pad_data(plaintext.encode('utf-8'))
    S = rc5_key_schedule(key_bytes)
    ciphertext = b''
    for i in range(0, len(data), 8):
        ciphertext += rc5_encrypt(data[i:i+8], S)
    return base64.b64encode(ciphertext).decode('utf-8')

def decrypt_text(ciphertext_b64, key):
    key_bytes = key.encode('utf-8')
    S = rc5_key_schedule(key_bytes)
    ciphertext = base64.b64decode(ciphertext_b64)
    plaintext = b''
    for i in range(0, len(ciphertext), 8):
        plaintext += rc5_decrypt(ciphertext[i:i+8], S)
    return plaintext.rstrip(b'\x00').decode('utf-8')

# ========== GUI ==========
root = Tk()
# Ukuran jendela
window_width = 600
window_height = 550

# Ambil ukuran layar
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Hitung posisi tengah
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)

# Atur posisi jendela
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

root.title("RC5 Email Encryption GUI")

frames = {}

def show_frame(name):
    for fname, frame in frames.items():
        frame.pack_forget()
    frames[name].pack(fill='both', expand=True)

# ========== Page 1: Menu ==========
frame1 = Frame(root)
frames['menu'] = frame1

Label(frame1, text="'Implementasi RC5 dalam Email'", font=("Arial", 20)).pack(pady=20)
Label(frame1, text="Pilih Mode", font=("Arial", 15)).pack(pady=20)
Button(frame1, text="Kirim Pesan (Enkripsi)", width=30, height=2, command=lambda: show_frame('encrypt')).pack(pady=20)
Button(frame1, text="Dekripsi Pesan", width=30, height=2, command=lambda: show_frame('decrypt')).pack(pady=20)

# ========== Page 2: Enkripsi & Kirim Email ==========
frame2 = Frame(root)
frames['encrypt'] = frame2

Label(frame2, text="Kirim Email Terenkripsi RC5", font=("Arial", 16)).pack(pady=10)

Rmail = StringVar()
Rpswrd = StringVar()
Rsender = StringVar()
Rsubject = StringVar()
Rkey = StringVar()

Label(frame2, text="Your Email:").pack()
Entry(frame2, textvariable=Rmail, width=50).pack()

Label(frame2, text="Password Aplikasi:").pack()
Entry(frame2, textvariable=Rpswrd, width=50, show="*").pack()

Label(frame2, text="Send to Email:").pack()
Entry(frame2, textvariable=Rsender, width=50).pack()

Label(frame2, text="Subject:").pack()
Entry(frame2, textvariable=Rsubject, width=50).pack()

Label(frame2, text="RC5 Key:").pack()
Entry(frame2, textvariable=Rkey, width=50).pack()

Label(frame2, text="Message:").pack()
msgbodyE = Text(frame2, width=50, height=10)
msgbodyE.pack()

def sendmail():
    try:
        plaintext = msgbodyE.get(1.0, 'end').strip()
        key = Rkey.get()
        if not key:
            messagebox.showerror("Error", "Key RC5 tidak boleh kosong.")
            return
        encrypted_message = encrypt_text(plaintext, key)

        msg = MIMEMultipart()
        msg['From'] = Rmail.get()
        msg['To'] = Rsender.get()
        msg['Subject'] = Rsubject.get()
        msg.attach(MIMEText(encrypted_message, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(Rmail.get(), Rpswrd.get())
        server.sendmail(Rmail.get(), Rsender.get(), msg.as_string())
        server.quit()
        messagebox.showinfo("Success", "Email berhasil dikirim!")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal mengirim email: {e}")

Button(frame2, text="Kirim", bg="green", fg="white", command=sendmail).pack(pady=10)
Button(frame2, text="Kembali ke Menu", command=lambda: show_frame('menu')).pack(pady=10)

# ========== Page 3: Dekripsi ==========
frame3 = Frame(root)
frames['decrypt'] = frame3

Label(frame3, text="Dekripsi Pesan RC5", font=("Arial", 16)).pack(pady=10)

Label(frame3, text="Masukkan Chipertext (base64):").pack()
cipher_input = Text(frame3, width=50, height=10)
cipher_input.pack()

Label(frame3, text="RC5 Key:").pack()
key_input = Entry(frame3, width=50)
key_input.pack()

def decrypt_action():
    try:
        ciphertext = cipher_input.get(1.0, 'end').strip()
        key = key_input.get()
        if not key:
            messagebox.showerror("Error", "Key tidak boleh kosong.")
            return
        plaintext = decrypt_text(ciphertext, key)
        messagebox.showinfo("Plaintext", plaintext)
    except Exception as e:
        messagebox.showerror("Error", f"Gagal mendekripsi: {e}")

Button(frame3, text="Dekripsi", bg="blue", fg="white", command=decrypt_action).pack(pady=10)
Button(frame3, text="Kembali ke Menu", command=lambda: show_frame('menu')).pack(pady=10)

# ========== Start GUI ==========
show_frame('menu')
root.mainloop()
