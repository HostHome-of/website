import smtplib
from os import environ as env
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def enviarEmail(usuario, archivo, t, ver: bool = False):

    message = MIMEMultipart("alternative")
    message["Subject"] = t
    message["From"] = env["EMAIL"]
    message["To"] = usuario["mail"]

    if not ver:
        f = open(archivo, "r").read()
        part2 = MIMEText(f, "html")
    else:
        part2 = MIMEText(archivo, "html")

    message.attach(part2)

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo() 
        smtp.starttls()
        smtp.ehlo()

        smtp.login(env["EMAIL"], env["EMAIL_PSW"])

        msg = message.as_string()

        smtp.sendmail(env["EMAIL"], usuario["mail"], msg)
        smtp.quit()