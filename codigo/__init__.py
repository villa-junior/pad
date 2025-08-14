import os
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Configurações da app
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Inicializa extensões
    db.init_app(app)
    migrate.init_app(app, db)

    # Importa blueprints e login_required (para usar nos endpoints abaixo)
    from .auth import bp_auth, login_required
    from .faleConosco import bp_fale_conosco
    from .atividades import bp_atividades

    # Registra blueprints
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_fale_conosco)
    app.register_blueprint(bp_atividades)

    # Rotas básicas
    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/forum")
    @login_required
    def forum():
        return render_template("forum.html")

    return app
