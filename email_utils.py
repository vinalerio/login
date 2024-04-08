#email_utils.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def enviar_correo(correo, password_temporal):
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
    body = f"Hola, tu contraseña temporal es: {password_temporal}"
    msg.attach(MIMEText(body, 'plain'))

    # Iniciar la conexión SMTP y enviar el correo
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls() # Inicia TLS
        server.login(smtp_username, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_username, correo, text)
        server.quit()
        print("Correo enviado exitosamente")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# Ejemplo de uso
correo_destinatario = "destinatario@exemplo.com"
password_temporal = "hklu0oju" # Ejemplo de contraseña temporal
enviar_correo(correo_destinatario, password_temporal)