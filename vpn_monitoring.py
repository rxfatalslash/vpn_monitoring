import re
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuración mail
mail_user = 'SENDER_MAIL'
mail_password = 'SENDER_PASSWORD'

dest_user = 'DEST_MAIL'
subject = "New VPN Connection"

# Archivo log OpenVPN
log_route = 'VPN_LOG_ROUTE'

def send_mail(mensaje):
    msg = MIMEMultipart()
    msg['From'] = mail_user
    msg['To'] = dest_user
    msg['Subject'] = subject

    msg.attach(MIMEText(mensaje, 'plain'))

    # Servidor SMTP
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login(mail_user, mail_password)
    smtp_server.sendmail(mail_user, dest_user, msg.as_string())
    smtp_server.quit()

def vpn_monitor():
    last_position = 0
    try:
        while True:
            with open(log_route, 'r') as log:
                log.seek(last_position)
                for line in log:
                    if re.search(f"Peer Connection Initiated with", line):
                        mensaje = f"A new connection to the VPN server has been detected"
                        send_mail(mensaje)

                last_position = log_tell()

            time.sleep(1)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    vpn_monitor()