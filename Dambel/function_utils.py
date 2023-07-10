import smtplib
from email.mime.text import MIMEText

import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()
email = env('EMAIL_HOST_USER')
psw = env('EMAIL_HOST_PASSWORD')


def send_email(subject, body, recipients, sender=email, password=psw):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
