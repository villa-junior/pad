import sqlite3
from flask import g
from typing import List
from models import Disciplina,Estudante,Professor

DATABASE = 'test.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    return conn

def insert_estudante_into_db(estudantes: List[Estudante], conn):
    """Insere estudantes no banco de dados, não faz nada se já existirem"""
    cursor = conn.cursor()
    for estudante in estudantes:
        # Verifica se o estudante já existe
        existente = cursor.execute(
            "SELECT 1 FROM Estudante WHERE matricula_estudante = ?",
            (estudante.matricula,)
        ).fetchone()
        
        if not existente:
            try:
                cursor.execute(
                    "INSERT INTO Estudante (matricula_estudante, nome) VALUES (?, ?)",
                    (estudante.matricula, estudante.nome)
                )
            except sqlite3.IntegrityError:
                pass  # Caso raro de concorrência, ignora
    conn.commit()

def insert_professores_into_db(professores: List[Professor], conn):
    """Insere professores no banco de dados, não faz nada se já existirem"""
    cursor = conn.cursor()
    for professor in professores:
        # Verifica se o professor já existe
        existente = cursor.execute(
            "SELECT 1 FROM Professor WHERE matricula_professor = ?",
            (professor.matricula,)
        ).fetchone()
        
        if not existente:
            try:
                cursor.execute(
                    "INSERT INTO Professor (matricula_professor, nome) VALUES (?, ?)",
                    (professor.matricula, professor.nome)
                )
            except sqlite3.IntegrityError:
                pass  # Caso raro de concorrência, ignora
    conn.commit()

def insert_disciplinas_into_db(disciplinas: List[Disciplina], conn):
    """Insere disciplinas e seus relacionamentos, não faz nada se já existirem"""
    cursor = conn.cursor()
    for disciplina in disciplinas:
        # Verifica se a disciplina já existe usando o id_disciplina
        disciplina_existente = cursor.execute(
            "SELECT disciplina_id FROM Disciplina WHERE disciplina_id = ?",
            (disciplina.id_disciplina,)
        ).fetchone()

        if not disciplina_existente:
            try:
                cursor.execute(
                    "INSERT INTO Disciplina (disciplina_id, sigla, nome) VALUES (?, ?, ?)",
                    (disciplina.id_disciplina, disciplina.sigla, disciplina.nome)
                )
            except sqlite3.IntegrityError:
                continue  # Disciplina foi inserida concorrentemente, pula para próxima

        # Insere professores (apenas se não existirem)
        if disciplina.professores:
            insert_professores_into_db(disciplina.professores, conn)
            for professor in disciplina.professores:
                # Verifica se o relacionamento já existe
                rel_existente = cursor.execute(
                    "SELECT 1 FROM Professor_Disciplina WHERE matricula_professor = ? AND disciplina_id = ?",
                    (professor.matricula, disciplina.id_disciplina)
                ).fetchone()
                
                if not rel_existente:
                    try:
                        cursor.execute(
                            "INSERT INTO Professor_Disciplina (matricula_professor, disciplina_id) VALUES (?, ?)",
                            (professor.matricula, disciplina.id_disciplina)
                        )
                    except sqlite3.IntegrityError:
                        pass  # Relação foi criada concorrentemente

        # Insere estudantes (apenas se não existirem)
        if disciplina.estudantes:
            insert_estudante_into_db(disciplina.estudantes, conn)
            for estudante in disciplina.estudantes:
                # Verifica se o relacionamento já existe
                rel_existente = cursor.execute(
                    "SELECT 1 FROM Estudante_Disciplina WHERE matricula_estudante = ? AND disciplina_id = ?",
                    (estudante.matricula, disciplina.id_disciplina)
                ).fetchone()
                
                if not rel_existente:
                    try:
                        cursor.execute(
                            "INSERT INTO Estudante_Disciplina (matricula_estudante, disciplina_id) VALUES (?, ?)",
                            (estudante.matricula, disciplina.id_disciplina)
                        )
                    except sqlite3.IntegrityError:
                        pass  # Relação foi criada concorrentemente

    conn.commit()

