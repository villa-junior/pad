import os
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import Base  # Base e models declarados no seu models.py

from auth import bp_auth, login_required
from faleConosco import bp_fale_conosco
from atividades import bp_atividades

load_dotenv() # carrega variáveis do .env

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# inicializacao do db e migrate com flask
db = SQLAlchemy(model_class=Base)
db.init_app(app)
migrate = Migrate(app, db)

# Blueprints
app.register_blueprint(bp_auth)
app.register_blueprint(bp_fale_conosco)
app.register_blueprint(bp_atividades)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/forum")
@login_required
def forum():
    return render_template("forum.html")

if __name__ == "__main__":
    app.run(debug=True)