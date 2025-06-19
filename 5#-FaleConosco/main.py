from flask import Flask,render_template,session,request,flash,g
from datetime import datetime

from database import get_db,close_db
from auth import login_required

app = Flask(__name__)

# Fecha conexão ao final de cada request
app.teardown_appcontext(close_db)
app.config.from_mapping(
        SECRET_KEY='dev'
)
from auth import bp
app.register_blueprint(bp) # adição das urls para autenticação

topicos = {
    1:"Calendário",
    2:"Cadastro",
    3:"Avaliações",
    4:"Outros"
}

@app.route("/")
def home():
    #print(session) 
    return render_template("home.html")

@login_required
@app.route("/reclamar",methods=('GET','POST'))
def reclamar():
    if request.method == 'POST':
        id_topico = request.form["id_topico"]
        descricao = request.form["descricao"]

        db = get_db()
        error = None

        if not g.user:
            error = 'Log in não realizado'
        elif not id_topico:
            error = 'Tópico necessário'
        elif not descricao:
            error = 'Descrição necessário'
        
        if error is None:
            data_atual = datetime.now().strftime("%d/%m/%Y")
            try:
                db.execute(
                    'INSERT INTO Reclamacao (matricula,id_topico,descricao,data_reclamacao) VALUES (?,?,?,?)', 
                    (g.user["matricula"],id_topico,descricao,data_atual)
                )
                db.commit()
            except db.IntegrityError:
                error = f"Erro inesperado"
        
        if error is not None: flash(error)
    return render_template("reclamar.html")

@app.route("/reclamacoes")
def reclamacoes():

    db = get_db()
    error = None

    reclamacoes = db.execute(
        'SELECT * FROM Reclamacao'
    )
    reclamacoes_top = [
    {**r, "topico_nome": topicos.get(r["id_topico"], "Desconhecido")}
    for r in reclamacoes
    ]

    if error is not None: flash(error)
    return render_template("reclamacoes.html",reclamacoes=reclamacoes_top)

if __name__ == "__main__":
    app.run()