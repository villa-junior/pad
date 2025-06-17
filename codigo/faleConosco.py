from datetime import datetime
from sqlalchemy import create_engine, Table, text, MetaData,insert
from database import engine,SessionLocal

metadata = MetaData()
reclamacoes_table = Table('Reclamacao', metadata, autoload_with=engine)
# acredito que seria mais coerente com o uso do sqlalchemy ter um models.py
# com classes que utilizam apenas ORM para interagir com a db

# uma boa prática seria criar um Enum para topico

def insert_reclamacao(matricula: int, topico: str, descricao: str):
    session = SessionLocal() # a abordagem com o session é mais comum no uso do flask
    data_atual = datetime.now().strftime("%Y-%m-%d")  # TODO: integrar isso diretamente no mysql
    
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
