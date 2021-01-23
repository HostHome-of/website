import smtplib
from os import environ as env
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def enviarEmail(usuario, archivo, t):

    message = MIMEMultipart("alternative")
    message["Subject"] = t
    message["From"] = env["EMAIL"]
    message["To"] = usuario["mail"]


    f = open(archivo, "r").read()
    part2 = MIMEText(f, "html")

    message.attach(part2)

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo() 
        smtp.starttls()
        smtp.ehlo()

        smtp.login(env["EMAIL"], env["EMAIL_PSW"])


        smtp.sendmail(env["EMAIL"], usuario["mail"], message.as_string())