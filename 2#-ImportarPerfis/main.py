from flask import Flask,render_template,session,request,flash,g
from typing import List
from models import Disciplina, Professor, Estudante
import argparse

from database import get_db,get_db_connection,close_db,insert_disciplinas_into_db
from acesso_suap import get_data
app = Flask(__name__)

# Fecha conexão ao final de cada request
app.teardown_appcontext(close_db)
app.config.from_mapping(
        SECRET_KEY='dev'
)
#from disciplina import bp
#app.register_blueprint(bp) # adição das urls para autenticação

def initialize_app():
    print("------------------------------------------------------------")
    print("Iniciando conexão com o SUAP")
        
    try:
        disciplinas: List[Disciplina] = get_data()  # Sua função para obter os dados
        print("Dados coletados com sucesso!")
        print("------------------------------------------------------------")
            
        #Conectar ao banco de dados
        db = get_db_connection()
        print("Conexão com o banco de dados estabelecida")
            
        # Inserir os dados
        print("Inserindo os dados na db....")
        insert_disciplinas_into_db(disciplinas=disciplinas, conn=db)
        print("Dados inseridos com sucesso!")
            
    except Exception as e:
        print(f"Erro durante o processo: {e}")
    finally:
        if 'db' in locals():
            db.close()
            print("Conexão com o banco de dados encerrada")
            print("------------------------------------------------------------")
            print("Processo concluído")
            print("------------------------------------------------------------")



@app.route("/")
def home():
    db = get_db()
    disciplinas = db.execute(
        "SELECT * FROM Disciplina"
    )

    return  render_template("home.html",disciplinas=disciplinas)

@app.route("/disciplina/<int:disciplina_id>")
def disciplina(disciplina_id: int): #TODO: isso aqui pode ser otimizado com JOIN, mas fica meio complicado de entender
    professores: List[Professor] = []
    estudantes: List[Estudante] = []
    
    db = get_db()

    disciplina = db.execute(
        "SELECT * FROM Disciplina WHERE disciplina_id = ?",
        (disciplina_id,)
    ).fetchone()

    m_professores = db.execute(
        "SELECT * FROM Professor_Disciplina WHERE disciplina_id = ?",
        (disciplina_id,)
    ).fetchall()

    for m_professor in m_professores:
        professor = db.execute(
            "SELECT * FROM Professor WHERE matricula_professor = ?",
            (m_professor["matricula_professor"],)
        ).fetchone()

        if professor:
            professores.append(Professor(
                matricula=professor["matricula_professor"],
                nome=professor["nome"]
            ))

    m_estudantes = db.execute(
        "SELECT * FROM Estudante_Disciplina WHERE disciplina_id = ?",
        (disciplina_id,)
    ).fetchall()

    for m_estudante in m_estudantes:
        estudante = db.execute(
            "SELECT * FROM Estudante WHERE matricula_estudante = ?",
            (m_estudante["matricula_estudante"],)
        ).fetchone()

        if estudante:
            estudantes.append(Estudante(
                matricula=estudante["matricula_estudante"],
                nome=estudante["nome"]
            ))

    return render_template(
        "disciplina.html",
        disciplina=disciplina,
        professores=professores,
        estudantes=estudantes
    )

@app.route("/professor/{matricula}")
def professor(matricula):
    return "Essa seria a página do professor {matricula}"

@app.route("/estudante/{matricula}")
def estudante(matricula):
    return "Essa seria a página do estudante {matricula}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--initialize",
        action="store_true",
        help="Busca informações do suap e salva na db"
    )
    args = parser.parse_args()

    if args.initialize: # caso usuario passe o parâmetro o sistema inicializará
        initialize_app()
    app.run()