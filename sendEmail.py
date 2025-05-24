import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#email program
email = "keamananinformasitugas@gmail.com"
#password email: sakitdadakukumulaimengeluh (hanya dipakai login gmail, tidak dipakai di kode program)
#password program:
password = "hwhe netp vzot eqcf" 
#email penerima:
send_to_email = "blablabla@gmail.com"
#email subjek email:
subject = "Tes Program 1"
#pesan
message = "Ini adalah isi email dari Python."

msg = MIMEMultipart()
msg['From'] = email
msg['To'] = send_to_email
msg['Subject'] = subject
msg.attach(MIMEText(message, 'plain'))

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, send_to_email, msg.as_string())
    server.quit()
    print("Email berhasil dikirim.")
except Exception as e:
    print("Terjadi error:", e)
