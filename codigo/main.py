from flask import Flask, render_template, request, redirect, url_for
from atividadespad import insert_atividade, get_atividades

app = Flask(__name__)


@app.route("/")
def index():
    return redirect(url_for("atividades"))

@app.route("/formulario")
def formulario():

    return render_template("formulario.html")

@app.route("/cadastrar_atividade", methods=['GET', 'POST'])
def cadastrar_atividade():

    
    materia = request.form.get('materia')
    assunto = request.form.get('assunto')
    data_hora_realizacao = request.form.get('data_hora_realizacao')
    docente_id = request.form.get('docente_id')
    tipo_atividade = request.form.get('tipo_atividade')
    forma_aplicacao = request.form.get('forma_aplicacao')
    links_material = request.form.get('links_material')
    permite_consulta = bool(request.form.get('permite_consulta'))
    pontuacao = request.form.get('pontuacao')
    local_prova = request.form.get('local_prova')
    materiais_necessarios = request.form.get('materiais_necessarios')
    outros_materiais = request.form.get('outros_materiais')
    avaliativa = bool(request.form.get('avaliativa'))

    return insert_atividade(
        materia, assunto, data_hora_realizacao, docente_id, tipo_atividade, forma_aplicacao,
        links_material, permite_consulta, pontuacao, local_prova, materiais_necessarios,
        outros_materiais, avaliativa
    )

@app.route("/atividades")
def atividades():
    atividades = get_atividades()
    return render_template("atividades.html", atividades=atividades)

if __name__ == "__main__":
    app.run(debug=True)