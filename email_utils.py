#C:\xampp\miapp\email_utils.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def enviar_correo(correo, cuerpo, password_temporal):
    # Configuración del servidor SMTP
    smtp_server = "smtp.copaco.com.py" # Reemplaza con tu servidor SMTP
    smtp_port = 587 # Puerto para conexión segura con TLS
    smtp_username = "suscripcion@copaco.com.py" # Reemplaza con tu usuario SMTP
    smtp_password = "2mGGw4]b" # Reemplaza con tu contraseña SMTP

    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = correo
    msg['Subject'] = "Bienvenida"
    msg.attach(MIMEText(cuerpo, 'plain'))

    # Iniciar la conexión SMTP y enviar el correo
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_username, correo, text)
        server.quit()
        print("Correo enviado exitosamente")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
