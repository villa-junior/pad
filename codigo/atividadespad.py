from sqlalchemy import create_engine, Table, text, MetaData
from sqlalchemy.orm import sessionmaker, Session



engine = create_engine('mysql+pymysql://root:123456*@localhost:3306/bancopad')
metadata = MetaData()
atividades = Table('Atividade', metadata,
                   autoload_with=engine)

def insert_atividade(materia, assunto, data_hora_realizacao, docente_id, tipo_atividade, forma_aplicacao,
              links_material, permite_consulta, pontuacao, local_prova, materiais_necessarios,
              outros_materiais, avaliativa):
    
    with engine.connect() as conn:
        
        conn.execute(atividades.insert().values(
            materia=materia,
            assunto=assunto,
            data_hora_realizacao=data_hora_realizacao,
            docente_id=docente_id,
            tipo_atividade=tipo_atividade,
            forma_aplicacao=forma_aplicacao,
            links_material=links_material,
            permite_consulta=permite_consulta,
            pontuacao=pontuacao,
            local_prova=local_prova,
            materiais_necessarios=materiais_necessarios,
            outros_materiais=outros_materiais,
            avaliativa=avaliativa
        ))
        conn.commit()

    return "atividade cadastrada com sucesso"


def get_atividades():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM Atividade"))
        atividades = result.fetchall()
    return atividades