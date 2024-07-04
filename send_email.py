import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Veritabanı bağlantısı oluşturma
def connect_db():
    conn = sqlite3.connect('database.db')  # Veritabanı dosyasının adını ve yolunu uygun şekilde belirtin
    return conn

# Verileri alıp e-posta gönderen fonksiyon
def send_email(data):
    # E-posta ayarları
    sender_email = "nuraysavasan2002@gmail.com"  # Gönderici e-posta adresi
    receiver_email = "nuraysavasan2002@gmail.com"  # Alıcı e-posta adresi
    password = "Asyahundevleti1"  # E-posta şifresi
    smtp_server = "smtp.gmail.com"  # SMTP sunucu adresi
    smtp_port = 587  # SMTP sunucu portu

    # E-posta içeriği oluşturma
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = "Database Records"

    # E-posta metni oluşturma
    email_text = ""
    for record in data:
        email_text += f"ID: {record[0]}, Name: {record[1]}, Surname: {record[2]}, Phone: {record[3]}\n"

    message.attach(MIMEText(email_text, 'plain'))

    # SMTP server bağlantısı kurma
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

# Ana fonksiyon
def main():
    conn = connect_db()
    cursor = conn.cursor()

    # Veritabanından her 5 veriyi alıp e-posta gönderme
    cursor.execute("SELECT * FROM contacts")  # Tablo adı ve sorgu koşullarını uygun şekilde belirtin
    data = cursor.fetchall()

    if len(data) > 0:
        send_email(data)
        print("Veriler e-posta olarak gönderildi.")
    else:
        print("Gönderilecek veri bulunamadı.")

    conn.close()

if __name__ == "__main__":
    main()
