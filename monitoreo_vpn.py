import re
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuración mail
mail_user = 'CORREO_EMISOR'
mail_password = 'CONTRASEÑA_EMISOR'

dest_user = 'CORREO_DESTINO'
subject = "Nueva conexión al servidor VPN"

# Archivo log OpenVPN
log_route = 'RUTA_LOG_VPN'

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
                        mensaje = f"Se ha detectado una nueva conexión al servidor VPN"
                        send_mail(mensaje)

                last_position = log_tell()

            time.sleep(1)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    vpn_monitor()