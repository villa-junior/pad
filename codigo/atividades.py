import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Select, text
from database import SessionLocal
from models import Atividade, TipoAtividade, FormaAplicacao, LocalProva, Turma
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

from auth import login_required
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
    session = SessionLocal()
    try:
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

        if verificar_atividade_dia(data_hora_realizacao, turma):
            return "Já existem 2 atividades cadastradas para essa turma nesse dia."
        session.add(nova_atividade)
        session.flush() 
        session.commit()
        return "Atividade cadastrada com sucesso"
    except SQLAlchemyError as e:
        session.rollback()
        raise Exception(f"Erro ao cadastrar atividade: {str(e)}")
    finally:
        session.close()

# TODO: retirar essas consultas sql daqui, fazer tudo em ORM
def get_atividades():
    session = SessionLocal()
    try:
        result = session.execute(text("SELECT * FROM Atividade ORDER BY data_hora_realizacao ASC"))
        return result.mappings().all()
    except Exception as e:
        raise Exception(f"Erro ao buscar atividades: {e}")
    finally:
        session.close()

def verificar_atividade(id: int):
    session = SessionLocal()
    try:
        atividade = session.execute(text("SELECT matricula FROM Atividade WHERE id = :id"), {'id': id}).fetchone()
        matricula = atividade[0]
        if not atividade:
            raise Exception("Atividade não encontrada")
        return matricula
    except SQLAlchemyError as e:
        raise Exception(f"Erro ao verificar atividade: {str(e)}")
    finally:
        session.close()

def verificar_atividade_dia(data_hora_realizacao, turma: Turma) -> bool:
    session = SessionLocal()
    try:
        atividades = session.execute(text("SELECT * FROM Atividade WHERE DATE(data_hora_realizacao) = DATE(:data_hora_realizacao) AND turma = :turma"),
                                     {'data_hora_realizacao': data_hora_realizacao, 'turma': turma.value}).fetchall()
        if len(atividades) >= 2:
            return True
        
        return False
    except SQLAlchemyError as e:
        raise Exception(f"Erro ao verificar atividade: {str(e)}")
    finally:
        session.close()

def delete_atividade(id: int):
    session = SessionLocal()
    try:
        result = session.execute(text("DELETE FROM Atividade WHERE id = :id"), {'id': id})
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise Exception(f"Erro ao excluir atividade: {str(e)}")
    finally:
        session.close()


# ENDPOINTS DE ATIVIDADES

@bp_atividades.route("/cadastrar", methods=['GET', 'POST'])
@login_required
def cadastrar_atividade():
    if request.method == 'POST':
        materia = request.form.get('materia')
        assunto = request.form.get('assunto')
        data_hora_realizacao = request.form.get('data_hora_realizacao')
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
        if error is not None: # captura erros do backend e adiciona na interface
            flash(error)

        # Verificação básica de campos obrigatórios
        if not g.user:
            error = 'Log in não realizado'

        # esse g.user representa o usuário logado e registrado nos cookies

        if not materia or not assunto or not data_hora_realizacao or not g.user["matricula"]:
            error = "Preencha todos os campos obrigatórios."
        else:
            try:
                flash(insert_atividade(
                    materia, assunto, data_hora_realizacao, g.user["matricula"], tipo_atividade, forma_aplicacao,
                    links_material, permite_consulta, pontuacao, local_prova, materiais_necessarios,
                    outros_materiais, avaliativa, turma
                ))
                error = "Atividade cadastrada com sucesso."
                return redirect(url_for('home'))  # ou outra rota pós-cadastro
            except Exception as e:
                error = f"Erro ao cadastrar atividade: {str(e)}" 

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
        if verificar_atividade(id) != g.user["matricula"]:
            return jsonify({"error": "Você não tem permissão para excluir esta atividade."}), 403
        
        delete_atividade(id)
        return jsonify({"message": "Atividade excluída com sucesso."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
