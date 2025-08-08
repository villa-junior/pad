from datetime import datetime
from sqlalchemy import create_engine, Table, text, MetaData,insert
from database import engine,SessionLocal
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from auth import login_required

metadata = MetaData()
reclamacoes_table = Table('Reclamacao', metadata, autoload_with=engine)

bp_fale_conosco = Blueprint('faleConosco', __name__, url_prefix='/faleConosco')

def insert_reclamacao(matricula: int, topico: str, descricao: str):
    session = SessionLocal() # a abordagem com o session é mais comum no uso do flask
    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    try:
        stmt = insert(reclamacoes_table).values(
                    matricula=matricula,
                    topico=topico,
                    descricao=descricao,
                    data_reclamacao=data_atual
                )
        session.execute(stmt)
        session.commit()
        return "Atividade cadastrada com sucesso"
    except Exception as e: # exceção para ser capturada na main
        session.rollback() # caso dê alguma merda a db volta atrás
        raise Exception(f"Erro ao cadastrar atividade: {e}")
    finally:
        session.close()


def get_reclamacao():
    session = SessionLocal()
    try:
        result = session.execute(text("SELECT * FROM Reclamacao"))
        return result.mappings().all()
    except Exception as e: # exceção para ser capturada na main
        raise Exception(f"Erro ao buscar atividades: {e}")
    finally:
        session.close()


# ENDPOINTS PARA FALECONOSCO

@bp_fale_conosco.route("/reclamar", methods=('GET', 'POST'))
@login_required
def post_reclamacoes_endpoint():
    if request.method == 'POST': # substituir pelo uso do FlaskWTF
        topico = request.form.get("topico")
        descricao = request.form.get("descricao")

        error = None

        if not g.user: # g é uma variavel global do Flask, uma das muitas esquisitices desse framework
            error = 'Log in não realizado'
        elif not topico:# captura erros do backend e adiciona na interface
            error = 'Tópico é obrigatório.'
        elif not descricao:
            error = 'Descrição é obrigatória.'

        if error is not None: # captura erros do backend e adiciona na interface
            flash(error)
        else:
            try:
                insert_reclamacao( # usar o type hint do python é bem útil nessas situações
                    matricula=g.user["matricula"], 
                    topico=topico,
                    descricao=descricao
                )
                flash("Reclamação enviada com sucesso.")
                return redirect(url_for("home"))  # ou outra rota após sucesso
            except Exception as e:
                error = f"Erro ao enviar reclamação: {str(e)}" # adiciona a exceção na variavel

    return render_template("form_reclamar.html")

@bp_fale_conosco.route("/reclamacoes")
@login_required
def get_reclamacoes_endpoint():
    try:
        reclamacoes_top = get_reclamacao()
    except Exception as e:
        flash(f"Erro ao buscar reclamações: {str(e)}")
        reclamacoes_top = []

    return render_template("reclamacoes.html", reclamacoes=reclamacoes_top)