from flask import Flask, render_template, url_for, session, request, redirect, flash, g, jsonify
from flask_mail import Mail, Message
from atividadespad import insert_atividade, get_atividades, delete_atividade, verificar_atividade
from faleConosco import insert_reclamacao, get_reclamacao
from database import close_db, get_db
from models import Turma, TipoAtividade, FormaAplicacao, LocalProva
from auth import bp, login_required

app = Flask(__name__)

# Configurações gerais
app.teardown_appcontext(close_db)
app.config.from_mapping(SECRET_KEY='dev')

# Configurações do Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'comunicao.pad@gmail.com'  # substitua pelo seu usuário real
app.config['MAIL_PASSWORD'] = 'uckp diel azuj hfdg'      # substitua pela sua senha real ou app password
app.config['MAIL_DEFAULT_SENDER'] = ('Sistema de Atividades', 'comunicao.pad@gmail.com')

mail = Mail(app)

app.register_blueprint(bp)

# Função para enviar notificações por e-mail para uma lista de alunos
def notificar_alunos(emails, atividade):
    with app.app_context():
        for email in emails:
            msg = Message(
                subject='📚 Nova Atividade Cadastrada',
                recipients=[email],
                body=f"Uma nova atividade foi cadastrada:\n\n"
                     f"Matéria: {atividade['materia']}\n"
                     f"Assunto: {atividade['assunto']}\n"
                     f"Data e hora: {atividade['data_hora']}\n"
                     f"\nAcesse o sistema para mais detalhes."
            )
            mail.send(msg)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/formulario")
@login_required
def formulario():
    return render_template("form_atividades.html")

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

                # Buscar emails de todos os alunos
                db = get_db()
                alunos = db.execute("SELECT email FROM Usuario").fetchall()
                emails_alunos = [aluno['email'] for aluno in alunos]

                atividade = {
                    'materia': materia,
                    'assunto': assunto,
                    'data_hora': data_hora_realizacao
                }

                notificar_alunos(emails_alunos, atividade)

                return render_template("atividade_cadastrada.html", materia=materia, assunto=assunto)

            except Exception as e:
                error = f"Erro ao cadastrar atividade: {str(e)}" 

        flash(error)

    return render_template("form_atividades.html")

@app.route("/atividades")
@login_required
def atividades():
    try:
        atividades = get_atividades()
    except Exception as e:
        flash(f"Erro ao buscar atividades: {str(e)}")
        atividades = []
    return render_template("atividades.html", atividades=atividades)

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
    if request.method == 'POST':
        topico = request.form.get("topico")
        descricao = request.form.get("descricao")
        error = None

        if not g.user:
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
                    matricula=g.user["matricula"], 
                    topico=topico,
                    descricao=descricao
                )
                flash("Reclamação enviada com sucesso.")
                return redirect(url_for("home"))
            except Exception as e:
                error = f"Erro ao enviar reclamação: {str(e)}"

    return render_template("form_reclamar.html")

@app.route("/reclamacoes")
@login_required
def get_reclamacoes_endpoint():
    try:
        reclamacoes_top = get_reclamacao()
    except Exception as e:
        flash(f"Erro ao buscar reclamações: {str(e)}")
        reclamacoes_top = []

    return render_template("reclamacoes.html", reclamacoes=reclamacoes_top)

if __name__ == "__main__":
    app.run(debug=True)
