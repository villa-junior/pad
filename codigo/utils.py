import string
import random
import smtplib # Permitir enviar emails por SMTP
from email.mime.text import MIMEText

import os
from dotenv import load_dotenv

EMAIL = os.getenv("EMAIL")
SENHA_APP = os.getenv("SENHA_APP")

def enviar_email(codigo:str,destinatario:str,subject:str):
    message = MIMEText(f'Seu código é:' \
            f'{codigo}')
    message['From'] = EMAIL
    message['To'] = destinatario
    message['Subject'] = subject

    mail_server = smtplib.SMTP('smtp.gmail.com',587)
    mail_server.starttls()
    mail_server.login(EMAIL, SENHA_APP)
    mail_server.send_message(message)
    mail_server.quit()

def gerar_cod_verificacao(size=6, chars=string.ascii_uppercase + string.digits)-> str:
    return ''.join(random.choice(chars) for _ in range(size))
    
