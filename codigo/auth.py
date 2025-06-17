import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, Table, text, MetaData,insert

from database import SessionLocal,engine

metadata = MetaData()
bp = Blueprint('auth', __name__, url_prefix='/auth')
usuarios_table = Table('Usuario', metadata, autoload_with=engine)

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
            session_db = SessionLocal()
            try:
                stmt = insert(usuarios_table).values(
                    matricula=matricula,
                    nome=nome,
                    email=email,
                    senha=generate_password_hash(senha)
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
    session.clear()
    return redirect(url_for('home'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
