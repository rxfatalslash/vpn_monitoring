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

def device_info(log_line):
    # Patrón de extracción de IP y SO
    ip_patron = r'\[client\] Peer Connection Initiated with \[AF_INET\]([^:]+):(\d+)'
    so_patron = r'peer_info: Client ([^ ]+)'

    # Buscar IP y SO
    match_ip = re.search(ip_patron, log_line)
    match_so = re.search(so_patron, log_line)

    ip = match_ip.group(1) if match_ip else None
    so = match_so.group(1) if match_so else None

    return ip, hostname, so

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
    last_line = ''
    try:
        while True:
            with open(log_route, 'r') as log_file:
                lines = log_file.readlines()

            new_lines = lines[len(last_line):]

            for line in new_lines:
                ip, so = device_info(line)
                if ip and so:
                    mensaje = f"Se ha detectado una nueva conexión al servidor VPN desde:\n\nIP: {ip}\nSO: {so}"
                    send_sms(mensaje)

            last_line = lines[-1]

            time.sleep(1)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    vpn_monitor()