import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Select, text
from sqlalchemy.orm import joinedload
from flask import (
    Blueprint, flash, g, redirect, render_template, request, 
    url_for, jsonify
)

from .auth import login_required
from . import db
from .models import PostForum, Usuario

bp_forum = Blueprint('forum', __name__, url_prefix='/forum')

def insert_post(matricula: str, titulo: str, descricao: str):
    try:
        novo_post = PostForum(
            matricula=matricula,
            titulo=titulo,
            descricao=descricao
        )
        db.session.add(novo_post)
        db.session.flush()
        db.session.commit()
        return novo_post # seria melhor retornar um json?
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Erro ao criar post: {str(e)}")

def get_posts():
    try:
        posts = db.session.query(PostForum)\
            .options(joinedload(PostForum.usuario))\
            .order_by(PostForum.data_post.desc())\
            .all()
        return posts
    except Exception as e:
        raise Exception(f"Erro ao buscar posts: {e}")

def verificar_post(id: int):
    try:
        post = db.session.query(PostForum).filter(PostForum.id_post == id).first()
        if not post:
            raise Exception("Post não encontrado")
        return post.matricula
    except SQLAlchemyError as e:
        raise Exception(f"Erro ao verificar post: {str(e)}")

def delete_post(id: int):
    try:
        post = db.session.query(PostForum).filter(PostForum.id_post == id).first()
        if post:
            db.session.delete(post)
            db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Erro ao excluir post: {str(e)}")

def mostrar_post(id: int):
    try:
        post = db.session.query(PostForum)\
            .options(joinedload(PostForum.usuario))\
            .filter(PostForum.id_post == id)\
            .first()

        return post 
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Erro ao mostrar post: {str(e)}")

# ENDPOINTS PARA FALECONOSCO

#Antes, baseado no tutorial do Miguel, dá para: padronizar os formulários usando o form.py, além de simplificar as rotas.
#2. Pasta app com todo o código. "from app import app" num arquivo chamado "pad.py". De lá, o arquivo __init__.py com as informações necessárias para iniciar.
#3. Atualizar requirements.

#TO DO:Fazer comentário e excluir postagem. Models para tabela de comentário.
#Comentário está ligado ao id do post, possui nome do usuario e matricula, id_comentario (rascunho).
@bp_forum.route('/')
@login_required
def forum():
    try:
        posts_top = get_posts()
    except Exception as e:
        flash(f'Erro ao carregar posts: {str(e)}', 'error')
        posts_top = []

    return render_template('forum/forum.html', posts=posts_top)

@bp_forum.route('/post_forum/<int:id>')
@login_required
def post_forum(id):
    try:
        post = mostrar_post(id)
        return render_template('forum/post_forum.html', post=post)
    except Exception as e:
        flash(f'Erro ao carregar post: {str(e)}', 'error')
        return redirect(url_for('forum'))

@bp_forum.route('/criar_post', methods=['GET', 'POST'])
@login_required
def criar_post():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')

        try:
            insert_post(g.user.matricula, titulo, descricao)
            flash('Post criado com sucesso!', 'success')
            return redirect(url_for('forum.forum'))
        except Exception as e:
            flash(f'Erro ao criar post: {str(e)}', 'error')

    return render_template('forum/form_forum.html')

@bp_forum.route('/excluir_post/<int:id>', methods=['DELETE'])
@login_required
def excluir_post(id):
    try:
        if not g.user: # implementar essa verificação em outros lugares
            return jsonify({"error": "Usuário não autenticado."}), 401
        if verificar_post(id) != g.user["matricula"]:
            return jsonify({"error": "Você não tem permissão para excluir este post."}), 403

        delete_post(id)
        return jsonify({"message": "Post excluído com sucesso."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400