from datetime import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from .auth import login_required
from .models import Reclamacao
from . import db  # importa objeto db do flask

bp_fale_conosco = Blueprint('faleConosco', __name__, url_prefix='/faleConosco')

def insert_reclamacao(matricula: int, topico: str, descricao: str):
    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M")

    try:
        nova_reclamacao = Reclamacao(
            matricula=matricula,
            topico=topico,
            descricao=descricao,
            data_reclamacao=data_atual
        )
        db.session.add(nova_reclamacao)
        db.session.commit()
        return "Reclamação adicionada com sucesso"
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Erro ao enviar reclamação: {e}")

def get_reclamacao():
    try:
        reclamacoes = db.session.query(Reclamacao).all()
        return reclamacoes
    except Exception as e:
        raise Exception(f"Erro ao buscar reclamações: {e}")


# ENDPOINTS PARA FALECONOSCO

@bp_fale_conosco.route("/reclamar", methods=('GET', 'POST'))
@login_required
def post_reclamacoes_endpoint():
    if request.method == 'POST':  # substituir pelo uso do FlaskWTF
        topico = request.form.get("topico")
        descricao = request.form.get("descricao")

        error = None

        if not g.user:  # g é variável global do Flask
            error = 'Log in não realizado'
        elif not topico:
            error = 'Tópico é obrigatório.'
        elif not descricao:
            error = 'Descrição é obrigatória.'

        if error is not None:
            flash(error)
        else:
            try:
                insert_reclamacao(
                    matricula=g.user.matricula,  # g.user como objeto
                    topico=topico,
                    descricao=descricao
                )
                flash("Reclamação enviada com sucesso.")
                return redirect(url_for("home"))  # ou outra rota após sucesso
            except Exception as e:
                flash(f"Erro ao enviar reclamação: {str(e)}")

    return render_template("faleConosco/form_reclamar.html")

@bp_fale_conosco.route("/reclamacoes")
@login_required
def get_reclamacoes_endpoint():
    try:
        reclamacoes_top = get_reclamacao()
    except Exception as e:
        flash(f"Erro ao buscar reclamações: {str(e)}")
        reclamacoes_top = []

    return render_template("faleConosco/reclamacoes.html", reclamacoes=reclamacoes_top)