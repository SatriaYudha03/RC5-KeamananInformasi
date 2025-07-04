from tkinter import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import messagebox
import base64
from rc5_simple import rc5_key_schedule, rc5_encrypt

# Fungsi bantu
def pad_data(data):
    while len(data) % 8 != 0:
        data += b'\x00'
    return data

def encrypt_text(plaintext, key):
    key_bytes = key.encode('utf-8')
    data = plaintext.encode('utf-8')
    data = pad_data(data)
    S = rc5_key_schedule(key_bytes)
    ciphertext = b''
    for i in range(0, len(data), 8):
        ciphertext += rc5_encrypt(data[i:i+8], S)
    return base64.b64encode(ciphertext).decode('utf-8')

# GUI setup
root = Tk()
root.geometry('500x700')
root.title("Email Sending GUI + RC5")

Label(root, text="Set Your Account", width=20, fg="green", font=("bold", 20)).place(x=90, y=20)

Rmail = StringVar()
Rpswrd = StringVar()
Rsender = StringVar()
Rsubject = StringVar()
Rkey = StringVar()

Label(root, text="Your Email Account:", width=20, font=("bold", 10)).place(x=40, y=90)
Entry(root, width=40, textvariable=Rmail).place(x=200, y=90)

Label(root, text="Your Password:", width=20, font=("bold", 10)).place(x=40, y=130)
Entry(root, width=40, textvariable=Rpswrd, show="*").place(x=200, y=130)

Label(root, text="Encryption Key (RC5):", width=20, font=("bold", 10)).place(x=40, y=170)
Entry(root, width=40, textvariable=Rkey).place(x=200, y=170)

Label(root, text="Compose", width=20, font=("bold", 15)).place(x=150, y=210)

Label(root, text="Sent to Email:", width=20, font=("bold", 10)).place(x=40, y=250)
Entry(root, width=40, textvariable=Rsender).place(x=200, y=250)

Label(root, text="Subject:", width=20, font=("bold", 10)).place(x=40, y=290)
Entry(root, width=40, textvariable=Rsubject).place(x=200, y=290)

Label(root, text="Message:", width=20, font=("bold", 10)).place(x=40, y=330)
msgbodyE = Text(root, width=30, height=10)
msgbodyE.place(x=200, y=330)

def sendmail():
    email = Rmail.get()
    password = Rpswrd.get()
    send_to_email = Rsender.get()
    subject = Rsubject.get()
    message = msgbodyE.get(1.0, 'end').strip()
    key = Rkey.get()

    if not all([email, password, send_to_email, subject, message, key]):
        messagebox.showerror("Error", "Semua field wajib diisi.")
        return

    try:
        encrypted_message = encrypt_text(message, key)

        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = send_to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(encrypted_message, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, send_to_email, msg.as_string())
        server.quit()

        messagebox.showinfo("Success", "Email berhasil dikirim dengan enkripsi RC5.")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal mengirim email:\n{e}")

Button(root, text="Send", width=20, bg='brown', fg="white", command=sendmail).place(x=180, y=620)

root.mainloop()
