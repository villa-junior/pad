
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Select, text
from database import SessionLocal
from models import Atividade, TipoAtividade, FormaAplicacao, LocalProva, Turma

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
            tipo_atividade=tipo_atividade,
            forma_aplicacao=forma_aplicacao,
            links_material=links_material,
            permite_consulta=permite_consulta,
            pontuacao=pontuacao,
            local_prova=local_prova,
            materiais_necessarios=materiais_necessarios,
            outros_materiais=outros_materiais,
            avaliativa=avaliativa,
            turma=turma
        )
        
        session.add(nova_atividade)
        session.flush() 
        session.commit()
        return "Atividade cadastrada com sucesso"
    except SQLAlchemyError as e:
        session.rollback()
        raise Exception(f"Erro ao cadastrar atividade: {str(e)}")
    finally:
        session.close()


def get_atividades():
    session = SessionLocal()
    try:
        result = session.execute(text("SELECT * FROM Atividade ORDER BY data_hora_realizacao ASC"))
        return result.mappings().all()
    except Exception as e:
        raise Exception(f"Erro ao buscar atividades: {e}")
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