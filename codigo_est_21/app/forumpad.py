import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Select, text
from sqlalchemy.orm import joinedload

from app.models import Post_Forum, Usuario
from app.database import SessionLocal

def insert_post(matricula: str, titulo: str, descricao: str):
    session = SessionLocal()
    try:
        novo_post = Post_Forum(
            matricula=matricula,
            titulo=titulo,
            descricao=descricao
        )
        session.add(novo_post)
        session.commit()
        return novo_post
    except Exception as e:
        session.rollback()
        raise Exception(f"Erro ao criar post: {str(e)}")
    finally:
        session.close()

def get_posts():
    session = SessionLocal()
    try:
        posts = session.query(Post_Forum)\
            .options(joinedload(Post_Forum.usuario))\
            .order_by(Post_Forum.data_post.desc())\
            .all()
        return posts
    except Exception as e:
        raise Exception(f"Erro ao buscar posts: {e}")
    finally:
        session.close()

def verificar_post(id: int):
    session = SessionLocal()
    try:
        post = session.query(Post_Forum).filter(Post_Forum.id_post == id).first()
        if not post:
            raise Exception("Post não encontrado")
        return post.matricula
    except SQLAlchemyError as e:
        raise Exception(f"Erro ao verificar post: {str(e)}")
    finally:
        session.close()

def delete_post(id: int):
    session = SessionLocal()
    try:
        post = session.query(Post_Forum).filter(Post_Forum.id_post == id).first()
        if post:
            session.delete(post)
            session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise Exception(f"Erro ao excluir post: {str(e)}")
    finally:
        session.close()

def mostrar_post(id: int):
    session = SessionLocal()
    try:
        post = session.query(Post_Forum)\
            .options(joinedload(Post_Forum.usuario))\
            .filter(Post_Forum.id_post == id)\
            .first()

        return post 
    except SQLAlchemyError as e:
        session.rollback()
        raise Exception(f"Erro ao mostrar post: {str(e)}")
    finally:
        session.close()