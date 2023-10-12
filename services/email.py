import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from email.header import Header
from dotenv import load_dotenv

load_dotenv()

# Configura los detalles del servidor SMTP de Gmail
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = os.getenv("SMTP_PORT")
smtp_username = os.getenv("SMTP_USERNAME")
smtp_password = os.getenv("SMTP_PASSWORD")

def send_email(supervisor_email, responsible_email, subject, responsible_name, habit, penalty):

    sender_email = smtp_username

    # Crea el objeto MIMEMultipart
    msg = MIMEMultipart()
    msg['From'] = formataddr((str(Header('CommitGrow', 'utf-8')), sender_email)) 
    msg['To'] = supervisor_email
    msg['Cc'] = responsible_email
    msg['Subject'] = subject

    # Agrega el cuerpo del mensaje
    msg.attach(MIMEText(get_email_body(responsible_name, habit, penalty), 'html'))

    # Establece una conexión segura con el servidor SMTP de Gmail
    try:
        print("Conectando con el servidor SMTP")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Envía el correo electrónico
        server.sendmail(sender_email, supervisor_email, msg.as_string())

        print("Correo electrónico enviado exitosamente")
    except Exception as e:
        print(f"Error al enviar el correo electrónico: {str(e)}")
    finally:
        print("Cerrando la conexión con el servidor SMTP")
        # Cierra la conexión con el servidor SMTP
        server.quit()

def get_email_body(responsible_name, habit, penalty):
    return """
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Notificación</title>
            <style>
                /* Estilos CSS */
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #ffffff;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }}
                h1 {{
                    color: #333333;
                }}
                p {{
                    color: #666666;
                }}
                .button {{
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #007bff;
                    color: #ffffff;
                    text-decoration: none;
                    border-radius: 4px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>¡{0} no ha cumplido!</h1>
                <p>Queremos informarte que {0} no ha cumplido con el compromiso pactado en el contrato.</p>
                <p>{0} se comprometió a realizar el hábito: <strong>{1}</strong></p>
                <p>Por su incumplimiento, deberá realizar la siguiente penalización:</p>
                <p>{2}</p>
                <p>Por favor, realiza la acción correspondiente.</p>
                <p>Gracias por tu atención.</p>
            </div>
        </body>
        </html>""".format(responsible_name, habit, penalty)
