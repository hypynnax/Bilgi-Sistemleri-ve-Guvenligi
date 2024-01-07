import threading
import time as tm
from tkinter import *
import random
import re
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import messagebox


code = ''
code_length = 6
recipient_email = ''
sender_email = 'nktkargo@gmail.com'
sender_email_password = 'luzs jusz gakl sabz'
time = 90
countdown = time


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


def generate_random_code(length=6):
    return ''.join(random.choice(string.digits) for _ in range(length))


def setting_time():
    global time, countdown
    while(countdown != 0):
        countdown -= 1
        duration.config(text=str(int(countdown/60)).zfill(2) + ':' + str(countdown%60).zfill(2))
        tm.sleep(1)


def send_mail():
    global code, recipient_email, countdown, sender_email, sender_email_password
    countdown = time
    code = generate_random_code(code_length)
    
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = sender_email
    smtp_password = sender_email_password

    subject = "Süreli Giriş Kodunuz"
    message = f"Kodunuz: {code}"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        messagebox.showinfo("Bilgilendirme", f"Kod e-posta ile gönderildi: {recipient_email}")
        with open("code.txt", "w") as file:
            file.write(code)
    except Exception as e:
        messagebox.showerror("Uyarı", "E-posta gönderme hatası")
        exit(1)


def send_code():
    global code_length, recipient_email
    if (mail_entry.get() != "") and (is_valid_email(mail_entry.get())):
        recipient_email = mail_entry.get()
        
        send_mail()

        size.config(height=120, width=350)
        mail_label.destroy()
        mail_entry.destroy()
        send_button.destroy()
        code_label = Label(size, text="Code", background=primary_color, foreground=text_color)
        code_label.place(x=50, y=30)        
        code_entry.place(x=100, y=30)
        code_entry.focus_set()
        refresh_button = Button(windows, text="⟲", background=secondary_color, foreground=text_color, activebackground=background_color, command=send_mail)
        refresh_button.place(x=280, y=27)
        duration.place(x=240, y=55)
        submit_button = Button(windows, text="SUBMİT", background=secondary_color, foreground=text_color, activebackground=background_color, command=verification)
        submit_button.place(x=157, y=80)

        thread = threading.Thread(target=setting_time)
        thread.daemon = True
        thread.start()


def verification():
    if countdown > 0:
        if code == code_entry.get():
            messagebox.showinfo("Bilgilendirme", "Giriş Kodu Onaylandı")
            exit(1)
        else:
            messagebox.showerror("Uyarı", "Yanlış Kod Girişinde Bulundunuz!\nLütfen Doğru Kodu Giriniz")
    else:
        messagebox.showerror("Uyarı", "Geçerli Süre İçinde Girmediniz!\nYeni Kod Talebinde Bulununuz")


def on_key_press(event):
    if event.keysym == "Return":
        if send_button.winfo_exists():
            send_code()
        else:
            verification()


primary_color = '#2D4A53'
secondary_color = '#161B22'
text_color = '#AFB3B7'
background_color = '#5A636A'

windows = Tk(className=" Verification Code")
windows.resizable(False, False)
windows.iconbitmap(default='verification.ico')

size = Canvas(windows, height=100, width=350, background=primary_color, highlightbackground=primary_color)
size.pack()

mail_label = Label(size, text="E-MAİL", background=primary_color, foreground=text_color)
mail_label.place(x=50, y=30)
mail_entry = Entry(windows, width=30, background=background_color, foreground=text_color)
mail_entry.place(x=100, y=30)
mail_entry.focus_set()
send_button = Button(windows, text="Send Code", background=secondary_color, foreground=text_color, activebackground=background_color, command=send_code)
send_button.place(x=157, y=60)
code_entry = Entry(windows, width=28, background=background_color, foreground=text_color)
duration = Label(size, text=str(int(countdown/60)).zfill(2) + ':' + str(countdown%60).zfill(2), background=primary_color, foreground=text_color)

windows.bind("<Key>", on_key_press)

windows.mainloop()
