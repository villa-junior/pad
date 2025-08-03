from flask import Flask, g
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# no futuro o ideal é criar um arquivo com todos os models, para realizar carregamento
# das tabelas sem a necessidade de .sql

DATABASE_URL = os.getenv("DATABASE_URL")
# adicionar um .env DATABASE_URL=mysql+pymysql://root:<senha_super_díficil>@78.142.242.83:3306/bancopad

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_engine():
    return engine

def get_db():
    if 'db' not in g:
        g.db = SessionLocal()
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
# para padronizar a 