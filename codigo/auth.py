from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
import functools
import os   
from .utils import gerar_cod_verificacao, enviar_email
from .models import Usuario
from . import db  # objeto SQLAlchemy do flask_sqlalchemy

bp_auth = Blueprint('auth', __name__, url_prefix='/auth')

@bp_auth.route('/register', methods=('GET', 'POST'))
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
            error = 'Email necessário.'
        elif not senha:
            error = 'Senha necessária.'

        if error is None:
            try:
                existing_user = db.session.query(Usuario).filter(
                    (Usuario.matricula == matricula) |
                    (Usuario.nome == nome) |
                    (Usuario.email == email)
                ).first()

                if existing_user:
                    if existing_user.matricula == matricula:
                        error = "Matrícula já registrada."
                    elif existing_user.nome == nome:
                        error = "Nome já registrado."
                    elif existing_user.email == email:
                        error = "Email já registrado."
                else:
                    codigo_gerado = gerar_cod_verificacao()
                    # gerando a mensagem do email
                    messagem = f"Seu codigo é {codigo_gerado}"
                    enviar_email(destinatario=email, subject="Verificação de Email", message=messagem)

                    session['registro_temp'] = {
                        'matricula': matricula,
                        'nome': nome,
                        'email': email,
                        'senha': generate_password_hash(senha)
                    }
                    session['codigo_verificacao'] = codigo_gerado

                    return redirect(url_for("auth.verificar_email_endpoint"))

            except Exception as e:
                error = f"Erro ao verificar dados: {str(e)}"

        flash(error)

    return render_template('auth/register.html')


@bp_auth.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        matricula = request.form['matricula']
        senha = request.form['senha']

        error = None

        try:
            user = db.session.query(Usuario).filter_by(matricula=matricula).first()

            if user is None:
                error = 'Matrícula não encontrada.'
            elif not check_password_hash(user.senha, senha):
                error = 'Senha incorreta.'
            
            if error is None:
                session.clear()
                session['matricula'] = user.matricula
                return redirect(url_for('home'))

        except Exception as e:
            error = f"Erro ao fazer login: {str(e)}"

        flash(error)

    return render_template('auth/login.html')


@bp_auth.route('/change_password', methods=('GET', 'POST'))
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

        try:
            user = db.session.query(Usuario).filter_by(matricula=matricula).first()

            if user is None:
                flash("Usuário não encontrado.")
                return redirect(url_for('auth.login'))

            if not check_password_hash(user.senha, senha_atual):
                flash("Senha atual incorreta.")
                return redirect(url_for('auth.change_password'))

            user.senha = generate_password_hash(nova_senha)
            db.session.commit()

            session.clear()
            flash("Senha alterada com sucesso.")
            return redirect(url_for('auth.login'))

        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao alterar senha: {str(e)}")
            return redirect(url_for('auth.change_password'))


    return render_template('auth/change_password.html')


@bp_auth.route('/verificar_email', methods=['GET', 'POST'])
def verificar_email_endpoint():

    contexto = None

    if 'registro_temp' in session:
        email = session['registro_temp']['email']
        contexto = 'cadastro'
    elif 'recuperacao_senha' in session:
        email = session['recuperacao_senha']
        contexto = 'recuperacao'
    else:
        flash("Sessão expirada ou acesso inválido.")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        codigo = request.form.get("codigo")
        codigo_esperado = session.get('codigo_verificacao')
    
        if codigo == codigo_esperado:
            try:
                if contexto == 'cadastro':
                    usuario = Usuario(
                        matricula=session['registro_temp']['matricula'],
                        nome=session['registro_temp']['nome'],
                        email=session['registro_temp']['email'],
                        senha=session['registro_temp']['senha']
                    )
                    db.session.add(usuario)
                    db.session.commit()

                    flash("Usuário registrado com sucesso!")
                    session.pop('registro_temp', None)
                    session.pop('codigo_verificacao', None)
                    return redirect(url_for('auth.login'))

                elif contexto == 'recuperacao':
                    flash("Código verificado com sucesso. Redefina sua senha.")
                    session.pop('codigo_verificacao', None)
                    return redirect(url_for('auth.reset_password'))

            except IntegrityError:
                db.session.rollback()
                flash("Matrícula ou email já registrados.")
            except Exception as e:
                db.session.rollback()
                flash(f"Erro: {e}")
        else:
            flash("Código incorreto!")

    return render_template("auth/verify_email.html", email=email)


@bp_auth.route('/recover_password', methods=['GET','POST'])
def recover_password():

    EMAIL = os.getenv("EMAIL")
    SENHA_APP = os.getenv("SENHA_APP")
    if request.method == 'POST':
        email = request.form.get('email')  

        try:
            user = db.session.query(Usuario).filter_by(email=email).first()

            if user is None:
                flash("Não existe nenhum usuário com este e-mail.")
                return redirect(url_for('auth.recover_password'))
            
            codigo_gerado = gerar_cod_verificacao()
            # gerando a mensagem do email
            messagem = f"Seu codigo é {codigo_gerado}"

            enviar_email(destinatario=email, subject="Verificação de Email", message=messagem)
        
            session['codigo_verificacao'] = codigo_gerado
            session['recuperacao_senha'] = email
            return redirect(url_for("auth.verificar_email_endpoint"))

        except Exception as e:
            flash(f"Erro ao tentar recuperar conta: {str(e)}")
            return redirect(url_for('auth.recover_password'))
    
    return render_template('auth/recover_password.html')
                        
@bp_auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if 'recuperacao_senha' not in session:
        flash("Sessão expirada ou inválida.")
        return redirect(url_for('auth.login'))

    email = session['recuperacao_senha']

    if request.method == 'POST':
        nova_senha = request.form.get('nova_senha')
        confirmar = request.form.get('confirmar_senha')

        if nova_senha != confirmar:
            flash("As senhas não coincidem.")
            return redirect(url_for('auth.reset_password'))

        try:
            user = db.session.query(Usuario).filter_by(email=email).first()
            if not user:
                flash("Usuário não encontrado.")
                return redirect(url_for('auth.login'))

            user.senha = generate_password_hash(nova_senha)
            db.session.commit()

            session.clear()
            flash("Senha alterada com sucesso.")
            return redirect(url_for('auth.login'))

        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao atualizar senha: {e}")

        return redirect(url_for('auth.reset_password'))

    return render_template("auth/reset_password.html")


@bp_auth.before_app_request
def load_logged_in_user():
    matricula = session.get('matricula')

    if matricula is None:
        g.user = None
    else:
        try:
            g.user = db.session.query(Usuario).filter_by(matricula=matricula).first()
        except:
            g.user = None


@bp_auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
