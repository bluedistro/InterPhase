from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import smtplib

def send_message(message=None, subject=None):

    senderAddr = "enter your email address here"
    toAddr = "enter your email address again here, unless you want to send notifications to another email"
    msg = MIMEMultipart()
    msg['From'] = senderAddr
    msg['To'] = toAddr
    msg['Subject'] = subject

    body = message
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(senderAddr, "Enter your Password here")
    text = msg.as_string()
    server.sendmail(senderAddr, toAddr, text)
    server.quit()
