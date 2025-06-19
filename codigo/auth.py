import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Table, text, MetaData,insert

import smtplib # Permitir enviar emails por SMTP
from email.mime.text import MIMEText

from database import SessionLocal,engine

import os
from dotenv import load_dotenv

metadata = MetaData()
bp = Blueprint('auth', __name__, url_prefix='/auth')
usuarios_table = Table('Usuario', metadata, autoload_with=engine)
# acredito que seria mais coerente com o uso do sqlalchemy ter um models.py
# com classes que utilizam apenas ORM para interagir com a db

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        matricula = request.form['matricula']
        nome = request.form['nome']
        email = request.form["email"]
        senha = request.form['senha']

        error = None

        if not matricula:
            error = 'Matrícula necessária.'
        elif not nome:
            error = 'Nome necessário.'
        elif not email:
            error = 'Email necessário. '
        elif not senha:
            error = 'Senha necessária.'

        if error is None:
            session_db = SessionLocal() # abordagem com session é a mais comum
            try:
                stmt = insert(usuarios_table).values(
                    matricula=matricula,
                    nome=nome,
                    email=email,
                    senha=generate_password_hash(senha) # criptografia básica
                )
                session_db.execute(stmt)
                session_db.commit()
                return redirect(url_for("auth.login"))
            except IntegrityError:
                session_db.rollback()
                error = f"Usuário {matricula} já foi registrado."
            except Exception as e:
                session_db.rollback()
                error = f"Erro inesperado: {str(e)}"
            finally:
                session_db.close()

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        matricula = request.form['matricula']
        senha = request.form['senha']

        error = None
        session_db = SessionLocal()

        try:
            result = session_db.execute(
                text("SELECT * FROM Usuario WHERE matricula = :matricula"),
                {'matricula': matricula}
            )
            user = result.mappings().first()

            if user is None:
                error = 'Matrícula não encontrada.'
            elif not check_password_hash(user['senha'], senha):
                error = 'Senha incorreta.'
            
            if error is None:
                session.clear()  # session do Flask
                session['matricula'] = user['matricula']
                return redirect(url_for('home'))

        except Exception as e:
            error = f"Erro ao fazer login: {str(e)}"
        finally:
            session_db.close()

        flash(error)

    return render_template('auth/login.html')


#def Alterar senha
@bp.route('/change_password', methods=('GET', 'POST'))
def change_password():
    if request.method == 'POST':
        matricula = session.get('matricula')
        senha_atual = request.form.get('current_password')
        nova_senha = request.form.get('new_password')
        confirmar_senha = request.form.get('confirm_password')

        if not all([matricula, senha_atual, nova_senha, confirmar_senha]):
            flash("Preencha todos os campos.")
            return redirect(url_for('auth.change_password'))

        if nova_senha != confirmar_senha:
            flash("As senhas novas não conferem.")
            return redirect(url_for('auth.change_password'))
        if nova_senha == senha_atual:
            flash("A nova senha não pode ser igual a anterior ")
            return redirect(url_for('auth.change_password'))

        session_db = None  
        try:
            session_db = SessionLocal()  

           
            result = session_db.execute(
                text("SELECT * FROM Usuario WHERE matricula = :matricula"),
                {'matricula': matricula}
            )
            user = result.mappings().first()

            if user is None:
                flash("Usuário não encontrado.")
                return redirect(url_for('auth.login'))

            if not check_password_hash(user['senha'], senha_atual):
                flash("Senha atual incorreta.")
                return redirect(url_for('auth.change_password'))

            hashed_new_password = generate_password_hash(nova_senha)
            session_db.execute(
                text("UPDATE Usuario SET senha = :senha WHERE matricula = :matricula"),
                {'senha': hashed_new_password, 'matricula': matricula}
            )
            session_db.commit()
            session.clear()
            flash("Senha alterada com sucesso.")
            return redirect(url_for('auth.login'))
          

        except Exception as e:
            flash(f"Erro ao alterar senha: {str(e)}")
            return redirect(url_for('auth.change_password'))

        finally:
            if session_db:  
                session_db.close()

    
    return render_template('auth/change_password.html')  

#def recuperar senha
#def recuperar senha
@bp.route('/recover_password', methods = ['GET','POST'])
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
                return redirect(url_for('auth.recover_password'))
            
            message = MIMEText(f'Email para recuperar a senha.' \
            'Acesse o link abaixo:' \
            'aaaa')
            message['From'] = EMAIL
            message['To'] = email
            message['Subject'] = 'Recuperação de conta'

            mail_server = smtplib.SMTP('smtp.gmail.com',587)
            mail_server.starttls()
            mail_server.login(EMAIL, SENHA_APP)
            mail_server.send_message(message)
            mail_server.quit()
            flash('Email enviado! Esperando a confirmação')


        except Exception as e:
            flash(f"Erro ao tentar recuperar conta: {str(e)}")
            return redirect(url_for('auth.recover_password'))

        finally:
            if session_db:
                session_db.close()

    
    return render_template('auth/recover_password.html')
            
            


# o session do flask é utilizado para acessar o "localStorage" a

@bp.before_app_request
def load_logged_in_user():
    matricula = session.get('matricula')

    if matricula is None:
        g.user = None
    else:
        session_db = SessionLocal()
        try:
            result = session_db.execute(
                text("SELECT * FROM Usuario WHERE matricula = :matricula"),
                {'matricula': matricula}
            )
            g.user = result.mappings().first()
        except:
            g.user = None
        finally:
            session_db.close()


@bp.route('/logout')
def logout():
    session.clear() # limpa a sessão e os cookies carregados
    return redirect(url_for('home'))


def login_required(view): # função que funciona como decorator (podendo modificar o comportamento de outras funções)
    @functools.wraps(view)  
    # neste caso, ele funciona recebendo alguma função (como o de acesso a algum componente do site), 
    # verificando se existe algum usuário logado na sessão e retornando para a página de login (caso não haja algum usuario)
    # ou seguindo com o funcionamento da função normalmente
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
