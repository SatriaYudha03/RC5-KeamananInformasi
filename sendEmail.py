from tkinter import *
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

root = Tk()
root.geometry('500x640')
root.title("Email Sending GUI")

Label_0 = Label(root, text="Set Your Account", width=20, fg="green", font=("bold", 20))
Label_0.place(x=90, y=33)

Label_1 = Label(root, text="Your Email Account:", width=20, font=("bold", 10))
Label_1.place(x=40, y=110)

Rmail = StringVar()
Rpswrd = StringVar()
Rsender = StringVar()
Rsubject = StringVar()

emailE = Entry(root, width=40, textvariable=Rmail)
emailE.place(x=200, y=110)

Label_2 = Label(root, text="Your Password:", width=20, font=("bold", 10))
Label_2.place(x=40, y=160)

passwordE = Entry(root, width=40, textvariable=Rpswrd, show="*")
passwordE.place(x=200, y=160)

compose = Label(root, text="Compose", width=20, font=("bold", 15))
compose.place(x=150, y=210)

Label_3 = Label(root, text="Send to Email:", width=20, font=("bold", 10))
Label_3.place(x=40, y=260)

senderE = Entry(root, width=40, textvariable=Rsender)
senderE.place(x=200, y=260)

Label_4 = Label(root, text="Subject:", width=20, font=("bold", 10))
Label_4.place(x=40, y=310)

subjectE = Entry(root, width=40, textvariable=Rsubject)
subjectE.place(x=200, y=310)

Label_5 = Label(root, text="Message:", width=20, font=("bold", 10))
Label_5.place(x=40, y=360)

msgbodyE = Text(root, width=30, height=10)
msgbodyE.place(x=200, y=360)

def sendmail():
    try:
        email = Rmail.get()
        password = Rpswrd.get()
        send_to_email = Rsender.get()
        subject = Rsubject.get()
        message = msgbodyE.get("1.0", END)

        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = send_to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, send_to_email, msg.as_string())
        server.quit()

        # Tampilkan pesan sukses
        messagebox.showinfo("Success", "Email berhasil dikirim.")
    except Exception as e:
        # Tampilkan pesan error
        messagebox.showerror("Error", f"Terjadi error:\n{e}")

Button(root, text="Send", width=20, bg='brown', fg="white", command=sendmail).place(x=180, y=570)

root.mainloop()
