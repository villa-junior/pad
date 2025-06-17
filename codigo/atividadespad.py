from sqlalchemy import create_engine, Table, text, MetaData,insert
from database import engine,SessionLocal

metadata = MetaData()
atividades = Table('Atividade', metadata, autoload_with=engine)

# uma boa prática seria criar um Enum para tipo_atividade, forma_aplicacao, local_prova etc.
def insert_atividade(materia, assunto, data_hora_realizacao, matricula, tipo_atividade, forma_aplicacao,
                     links_material, permite_consulta, pontuacao, local_prova, materiais_necessarios,
                     outros_materiais, avaliativa):
    session = SessionLocal() # a abordagem com o session é mais comum no uso do flask
    try:
        stmt = insert(atividades).values(
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
                avaliativa=avaliativa
            )
        session.execute(stmt)
        session.commit()
        return "Atividade cadastrada com sucesso"
    except Exception as e:
        session.rollback()
        raise Exception(f"Erro ao cadastrar atividade: {e}")
    finally:
        session.close()

def get_atividades():
    session = SessionLocal()
    try:
        result = session.execute(text("SELECT * FROM Atividade"))
        return result.mappings().all()
    except Exception as e:
        raise Exception(f"Erro ao buscar atividades: {e}")
    finally:
        session.close()