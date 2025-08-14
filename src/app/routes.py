from flask import Flask,render_template,url_for,session,request,redirect,flash,g, jsonify

from app import app
from app.forumpad import insert_post, get_posts, verificar_post, delete_post, mostrar_post
from app.atividadespad import insert_atividade, get_atividades, delete_atividade, verificar_atividade
from app.faleConosco import insert_reclamacao,get_reclamacao
from app.database import close_db
from app.models import Turma, TipoAtividade, FormaAplicacao, LocalProva

from app.routes_auth import bp,login_required

@app.route("/")
def home():
    #print(session) 
    return render_template("home.html")

@app.route("/formulario")
@login_required
def formulario():
    return render_template("1_atividades/form_atividades.html")

@app.route("/cadastrar_atividade", methods=['GET', 'POST'])
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
        if error is not None:
            flash(error)

        if not g.user:
            error = 'Log in não realizado'

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
                return redirect(url_for('home'))
            except Exception as e:
                error = f"Erro ao cadastrar atividade: {str(e)}" 

    return render_template("1_atividades/form_atividades.html")

@app.route("/atividades")
@login_required
def atividades():
    try:
        atividades = get_atividades()
    except Exception as e:
        flash(f"Erro ao buscar atividades: {str(e)}")
        atividades = []
    return render_template("1_atividades/atividades.html", atividades=atividades)

@app.route('/atividades/<int:id>', methods=['DELETE'])
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

@app.route("/reclamar", methods=('GET', 'POST'))
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
                return redirect(url_for("home"))
            except Exception as e:
                error = f"Erro ao enviar reclamação: {str(e)}"

    return render_template("4_reclamacao/form_reclamar.html")

@app.route("/reclamacoes")
@login_required
def get_reclamacoes_endpoint():
    try:
        reclamacoes_top = get_reclamacao()
    except Exception as e:
        flash(f"Erro ao buscar reclamações: {str(e)}")
        reclamacoes_top = []

    return render_template("4_reclamacao/reclamacoes.html", reclamacoes=reclamacoes_top)

#Antes, baseado no tutorial do Miguel, dá para: padronizar os formulários usando o form.py, além de simplificar as rotas.
#2. Pasta app com todo o código. "from app import app" num arquivo chamado "pad.py". De lá, o arquivo __init__.py com as informações necessárias para iniciar.
#3. Atualizar requirements.

#TO DO:Fazer comentário e excluir postagem. Models para tabela de comentário.
#Comentário está ligado ao id do post, possui nome do usuario e matricula, id_comentario (rascunho).
@app.route('/forum')
def forum():
    try:
        posts_top = get_posts()
    except Exception as e:
        flash(f'Erro ao carregar posts: {str(e)}', 'error')
        posts_top = []

    return render_template('3_forum/forum.html', posts=posts_top)

@app.route('/post_forum/<int:id>')
def post_forum(id):
    try:
        post = mostrar_post(id)
        return render_template('3_forum/post_forum.html', post=post)
    except Exception as e:
        flash(f'Erro ao carregar post: {str(e)}', 'error')
        return redirect(url_for('forum'))

@app.route('/criar_post', methods=['GET', 'POST'])
def criar_post():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        matricula = session.get('matricula')
        
        try:
            insert_post(matricula, titulo, descricao)
            flash('Post criado com sucesso!', 'success')
            return redirect(url_for('forum'))
        except Exception as e:
            flash(f'Erro ao criar post: {str(e)}', 'error')
    
    return render_template('3_forum/form_forum.html')

@app.route('/excluir_post/<int:id>', methods=['DELETE'])
@login_required
def excluir_post(id):
    try:
        if not g.user:
            return jsonify({"error": "Usuário não autenticado."}), 401
        if verificar_atividade(id) != g.user["matricula"]:
            return jsonify({"error": "Você não tem permissão para excluir este post."}), 403
        
        delete_post(id)
        return jsonify({"message": "Post excluído com sucesso."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400