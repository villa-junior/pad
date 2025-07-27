from flask import Blueprint, render_template, request, jsonify
from models import Evento, ProgramacaoEvento, ParticipacaoEvento
from datetime import datetime

bp_calendario = Blueprint('calendario', __name__, url_prefix='/calendario')

@bp_calendario.route('/')
def calendario_view():
    return render_template('calendario.html')

@bp_calendario.route('/eventos/<string:data>', methods=['GET'])
def eventos_por_data(data):
    data_obj = datetime.strptime(data, '%Y-%m-%d').date()
    eventos = Evento.query.filter(Evento.data_inicio <= data_obj, Evento.data_fim >= data_obj).all()

    resultado = []
    for evento in eventos:
        programacoes = ProgramacaoEvento.query.filter_by(evento_id=evento.id).all()
        resultado.append({
            'evento': {
                'id': evento.id,
                'titulo': evento.titulo,
                'descricao': evento.descricao,
                'data_inicio': str(evento.data_inicio),
                'data_fim': str(evento.data_fim)
            },
            'programacao': [{

                'inicio': str(p.horario_inicio),
                'fim': str(p.horario_fim),
                'tema': p.tema,
                'organizador': p.organizador,
                'descricao': p.descricao
            } for p in programacoes]
        })

    return jsonify(resultado)
@bp_calendario.route('/evento', methods=['POST'])
def criar_evento():
    data = request.json
    try:
        evento = Evento(
            titulo=data['titulo'],
            descricao=data['descricao'],
            data_inicio=datetime.strptime(data['data_inicio'], '%Y-%m-%d').date(),
            data_fim=datetime.strptime(data['data_fim'], '%Y-%m-%d').date()
        )
        db.session.add(evento)
        db.session.commit()

        # Se quiser já criar programações junto, pode receber lista
        programacoes = data.get('programacoes', [])
        for p in programacoes:
            prog = ProgramacaoEvento(
                evento_id=evento.id,
                horario_inicio=datetime.strptime(p['inicio'], '%H:%M').time(),
                horario_fim=datetime.strptime(p['fim'], '%H:%M').time(),
                tema=p['tema'],
                organizador=p['organizador'],
                descricao=p['descricao']
            )
            db.session.add(prog)
        db.session.commit()

        return jsonify({'status': 'ok', 'evento_id': evento.id})

    except Exception as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)}), 400
