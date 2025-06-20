from atividadespad import insert_atividade, get_atividades, delete_atividade, verificar_atividade
from flask import Flask,render_template,url_for,session,request,redirect,flash,g, jsonify
from faleConosco import insert_reclamacao,get_reclamacao
from database import close_db
from models import Turma, TipoAtividade, FormaAplicacao, LocalProva

from auth import bp,login_required

app = Flask(__name__)

# Fecha conexão ao final de cada request
app.teardown_appcontext(close_db)
app.config.from_mapping(
        SECRET_KEY='dev' # usada na criptografação do cookies (dados de login)
)
app.register_blueprint(bp) # adição das urls para autenticação

@app.route("/")
def home():
    #print(session) 
    return render_template("home.html")

# no futuro seria ideal implementar um função genérica para tratar todas requisições e
# implementando o tratamento de erros correto com a HTTPException (404,403,500 etc.)

# acho que seria legal unir esses dois endpoints, afinal "formulario" é muito genérico
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
                insert_atividade(
                    materia, assunto, data_hora_realizacao, g.user["matricula"], tipo_atividade, forma_aplicacao,
                    links_material, permite_consulta, pontuacao, local_prova, materiais_necessarios,
                    outros_materiais, avaliativa, turma
                )
                error = "Atividade cadastrada com sucesso."
                return redirect(url_for('home'))  # ou outra rota pós-cadastro
            except Exception as e:
                error = f"Erro ao cadastrar atividade: {str(e)}" 

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
                return redirect(url_for("home"))  # ou outra rota após sucesso
            except Exception as e:
                error = f"Erro ao enviar reclamação: {str(e)}" # adiciona a exceção na variavel

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