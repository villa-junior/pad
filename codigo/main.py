from flask import Flask,render_template
from database import close_db

from auth import bp_auth,login_required
from faleConosco import bp_fale_conosco
from atividades import bp_atividades

app = Flask(__name__)

# Fecha conexão ao final de cada request
app.teardown_appcontext(close_db)
app.config.from_mapping(
        SECRET_KEY='dev' # usada na criptografação do cookies (dados de login)
)

# adição de blueprints, separando os endpoints e métodos de cada um grupo num arquivo separado
app.register_blueprint(bp_auth)
app.register_blueprint(bp_fale_conosco)
app.register_blueprint(bp_atividades)

@app.route("/")
def home():
    return render_template("home.html")

# no futuro seria ideal implementar um função genérica para tratar todas requisições e
# implementando o tratamento de erros correto com a HTTPException (404,403,500 etc.)

@app.route("/forum")
@login_required
def forum():
    return render_template("forum.html")

if __name__ == "__main__":
    app.run(debug=True)