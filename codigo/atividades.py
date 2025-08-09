import datetime
from sqlalchemy.exc import SQLAlchemyError
from .models import Atividade, TipoAtividade, FormaAplicacao, LocalProva, Turma
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from . import db
from .auth import login_required
from sqlalchemy import func, cast, Date

bp_atividades = Blueprint('atividades', __name__, url_prefix='/atividades')

def insert_atividade(
    materia: str,
    assunto: str,
    data_hora_realizacao,
    matricula: str,
    tipo_atividade: TipoAtividade,
    forma_aplicacao: FormaAplicacao,
    links_material: str,
    permite_consulta: bool,
    pontuacao,
    local_prova: LocalProva,
    materiais_necessarios: str,
    outros_materiais: str,
    avaliativa: bool,
    turma: Turma
):
    try:
        if verificar_atividade_dia(data_hora_realizacao, turma):
            return "Já existem 2 atividades cadastradas para essa turma nesse dia."

        nova_atividade = Atividade(
            materia=materia,
            assunto=assunto,
            data_hora_realizacao=data_hora_realizacao,
            matricula=matricula,
            tipo_atividade=tipo_atividade.value,
            forma_aplicacao=forma_aplicacao.value,
            links_material=links_material,
            permite_consulta=permite_consulta,
            pontuacao=pontuacao,
            local_prova=local_prova.value,
            materiais_necessarios=materiais_necessarios,
            outros_materiais=outros_materiais,
            avaliativa=avaliativa,
            turma=turma.value
        )

        db.session.add(nova_atividade)
        db.session.flush()
        db.session.commit()
        return "Atividade cadastrada com sucesso"
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Erro ao cadastrar atividade: {str(e)}")

def get_atividades() -> list[Atividade]:
    try:
        atividades = db.session.query(Atividade).order_by(Atividade.data_hora_realizacao.asc()).all()
        if not atividades:
            raise Exception("Atividade não encontrada")
        return atividades
    except Exception as e:
        raise Exception(f"Erro ao buscar atividades: {e}")

def verificar_atividade(id: int) -> str:
    try:
        atividade = db.session.query(Atividade).filter_by(id=id).first()
        if not atividade:
            raise Exception("Atividade não encontrada")
        return atividade.matricula
    except Exception as e: 
        raise Exception(f"Erro ao verificar atividade: {str(e)}")

def verificar_atividade_dia(data_hora_realizacao, turma: Turma) -> bool:
    try:
        atividades = db.session.query(Atividade).filter(
            cast(Atividade.data_hora_realizacao, Date) == data_hora_realizacao.date(),
            Atividade.turma == turma.value
        ).all()
        return len(atividades) >= 2
    except Exception as e:
        raise Exception(f"Erro ao verificar atividade: {str(e)}")

def delete_atividade(id: int):
    try:
        atividade = db.session.query(Atividade).filter_by(id=id).first()
        if not atividade:
            raise Exception("Atividade não encontrada para exclusão")
        db.session.delete(atividade)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Erro ao excluir atividade: {str(e)}")


# ENDPOINTS DE ATIVIDADES

@bp_atividades.route("/cadastrar", methods=['GET', 'POST'])
@login_required
def cadastrar_atividade():
    if request.method == 'POST':
        materia = request.form.get('materia')
        assunto = request.form.get('assunto')
        data_hora_realizacao_str = request.form.get('data_hora_realizacao')
        tipo_atividade = TipoAtividade(request.form.get("tipo_atividade"))
        forma_aplicacao = FormaAplicacao(request.form.get("forma_aplicacao"))
        links_material = request.form.get('links_material')
        permite_consulta = bool(request.form.get('permite_consulta'))
        pontuacao = request.form.get('pontuacao')
        local_prova = LocalProva(request.form.get('local_prova'))
        materiais_necessarios = request.form.get('materiais_necessarios')
        outros_materiais = request.form.get('outros_materiais')
        avaliativa = bool(request.form.get('avaliativa'))
        turma = Turma(request.form.get('turma'))
        error = None

        if not g.user:
            error = 'Login não realizado'

        # Converter data_hora_realizacao para datetime
        try:
            data_hora_realizacao = datetime.datetime.fromisoformat(data_hora_realizacao_str)
        except Exception:
            error = "Data e hora inválidas."

        if not materia or not assunto or not data_hora_realizacao_str or not g.user or not g.user.matricula:
            error = "Preencha todos os campos obrigatórios."

        if error is not None:
            flash(error)
        else:
            try:
                msg = insert_atividade(
                    materia, assunto, data_hora_realizacao, g.user.matricula, tipo_atividade, forma_aplicacao,
                    links_material, permite_consulta, pontuacao, local_prova, materiais_necessarios,
                    outros_materiais, avaliativa, turma
                )
                flash(msg)
                return redirect(url_for('home'))  # ou outra rota pós-cadastro
            except Exception as e:
                flash(f"Erro ao cadastrar atividade: {str(e)}") 

    return render_template("form_atividades.html")

@bp_atividades.route("/visualizar")
@login_required
def atividades():
    try:
        atividades = get_atividades()
    except Exception as e:
        flash(f"Erro ao buscar atividades: {str(e)}")
        atividades = []
    return render_template("atividades.html", atividades=atividades)

@bp_atividades.route('/visualizar/<int:id>', methods=['DELETE'])
@login_required
def excluir_atividade(id):
    try:
        if not g.user:
            return jsonify({"error": "Usuário não autenticado."}), 401
        if verificar_atividade(id) != g.user.matricula:
            return jsonify({"error": "Você não tem permissão para excluir esta atividade."}), 403
        
        delete_atividade(id)
        return jsonify({"message": "Atividade excluída com sucesso."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
