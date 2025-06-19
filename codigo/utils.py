
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from sqlalchemy import Table, text, MetaData

import smtplib # Permitir enviar emails por SMTP
from email.mime.text import MIMEText
from database import SessionLocal,engine
import os
import string
import random


metadata = MetaData()
utils_bp = Blueprint('utils', __name__, url_prefix='/utils')
usuarios_table = Table('Usuario', metadata, autoload_with=engine)

#def recuperar senha
@utils_bp.route('/recover_password', methods = ['GET','POST'])
def recover_password():

    EMAIL = os.getenv("EMAIL")
    SENHA_APP = os.getenv("SENHA_APP")
    if request.method == 'POST':
        email = request.form.get('email')  

        session_db = None
        try:
            session_db = SessionLocal()  

            result = session_db.execute(
                text("SELECT * FROM Usuario WHERE email = :email"),
                {'email': email}
            )
            user = result.mappings().first()

            if user is None:
                flash("Não existe nenhum usuário com este e-mail.")
                return redirect(url_for('utils.recover_password'))
            codigo_verificacao = gerar_cod_verificacao
            message = MIMEText(f'Seu código:' \
            f'{codigo_verificacao()}')
            message['From'] = EMAIL
            message['To'] = email
            message['Subject'] = 'Recuperação de conta'

            mail_server = smtplib.SMTP('smtp.gmail.com',587)
            mail_server.starttls()
            mail_server.login(EMAIL, SENHA_APP)
            mail_server.send_message(message)
            mail_server.quit()
            flash('Email enviado! Esperando a confirmação')
            return redirect(url_for('utils.recover_password'))

        except Exception as e:
            flash(f"Erro ao tentar recuperar conta: {str(e)}")
            return redirect(url_for('utils.recover_password'))

        finally:
            if session_db:
                session_db.close()

    
    return render_template('utils/recover_password.html')

def gerar_cod_verificacao(size=6, chars= string.ascii_uppercase + string.digits) -> str:
    return ''.join(random.choice(chars)for _ in range(size))
