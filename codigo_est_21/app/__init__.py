from flask import Flask,render_template,url_for,session,request,redirect,flash,g,jsonify

from app.faleConosco import insert_reclamacao,get_reclamacao
from app.atividadespad import insert_atividade, get_atividades,delete_atividade,verificar_atividade
from app.database import close_db
from app.models import Turma, TipoAtividade, FormaAplicacao, LocalProva

from app.routes_auth import bp, login_required

app = Flask(__name__)

app.teardown_appcontext(close_db)
app.config.from_mapping(
        SECRET_KEY='dev' # Usada na criptografa? do cookies (dados de login)
)
app.register_blueprint(bp) # Adição das urls para autenticação

from app import routes

"""
No futuro seria ideal implementar um função genérica para tratar todas requisiões e
implementando o tratamento de erros correto com a HTTPException (404,403,500 etc.).

"""
