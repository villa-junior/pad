import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from database import get_db

bp = Blueprint('auth',__name__, url_prefix='/auth') # todos os links desta página vão estar dentro do /auth

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        matricula = request.form['matricula']
        nome = request.form['nome']
        senha = request.form['senha']
        
        print(matricula,nome,senha)
        db = get_db()
        error = None

        if not matricula:
            error = 'Matrícula necessária.'
        elif not nome:
            error = 'Nome necessário'
        elif not senha:
            error = 'Senha necessária'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO Usuario (matricula,nome, senha) VALUES (?, ?, ?)",
                    (matricula, nome, generate_password_hash(senha)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Usuário {matricula} já foi registrado."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login',methods=('GET','POST'))
def login():
    if request.method == 'POST':
        matricula = request.form['matricula']
        senha = request.form['senha']

        db = get_db()
        error = None
        
        user = db.execute(
            'SELECT * FROM Usuario WHERE matricula = ?', (matricula,)
        ).fetchone()

        if user is None:
            error = 'Matrícula não encontrada'
        elif not check_password_hash(user['senha'], senha):
            error = 'Senha incorreta'

        if error is None: 
            session.clear()
            session['matricula'] = user['matricula'] # cookie passado para o navegador utilizar noutras opções
            return redirect(url_for('home'))
        
        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request # comando rodado antes de qualquer request, serve para carregar as informações do usuario caso ele já tenha realizado login
def load_logged_in_user():
    matricula = session.get('matricula')

    if matricula is None:
        g.user = None
    else:
        g.user = get_db().execute( 
            'SELECT * FROM Usuario WHERE matricula = ?', (matricula,)
        ).fetchone()

@bp.route('/logout')
def logout(): # responsável por remover o id do user da session e redirecionar para a página inicial
    session.clear()
    return redirect(url_for('home'))

def login_required(view): # função que funciona como decorator (podendo modificar o comportamento de outras funções)
    @functools.wraps(view) # neste caso, ele funciona recebendo alguma função (como o de acesso a algum componente do site), verificando se existe algum usuário
    # logado na sessão e retornando para a página de login (caso não haja algum usuario) ou seguindo com o funcionamento da função normalmente
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

