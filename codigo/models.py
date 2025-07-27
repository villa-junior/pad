from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, Text, DECIMAL, ForeignKey, Enum as SAEnum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TipoAtividade(enum.Enum):
    Prova_Objetiva = "Prova Objetiva"
    Prova_Discursiva = "Prova Discursiva"
    Prova_Mista = "Prova Mista"
    Seminario = "Seminário"
    Lista_de_Atividades = "Lista de Atividades"


class FormaAplicacao(enum.Enum):
    Individual = "Individual"
    Em_Dupla = "Em Dupla"
    Em_Grupo = "Em Grupo"


class LocalProva(enum.Enum):
    Sala_de_Aula = "Sala de Aula"
    Laboratorio = "Laboratório"
    AVA = "AVA"
    Ginasio = "Ginásio"

class Turma(enum.Enum):
    Informatica_1A = "1º A Informática"
    Informatica_1B = "1º B Informática"
    Informatica_1C = "1º C Informática"
    Informatica_2A = "2º A Informática"
    Informatica_2B = "2º B Informática"
    Informatica_2C = "2º C Informática"
    Informatica_3A = "3º A Informática"
    Informatica_3B = "3º B Informática"
    Informatica_3C = "3º C Informática"

    Edificacoes_1A = "1º A Edificações"
    Edificacoes_1B = "1º B Edificações"
    Edificacoes_2A = "2º A Edificações"
    Edificacoes_2B = "2º B Edificações"
    Edificacoes_3A = "3º A Edificações"


class Usuario(Base):
    __tablename__ = "Usuario"

    matricula = Column(String(20), primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)

    atividades = relationship("Atividade", back_populates="usuario", cascade="all, delete-orphan")


class Atividade(Base):
    __tablename__ = "Atividade"

    id = Column(Integer, primary_key=True, autoincrement=True)
    materia = Column(String(255), nullable=False)
    assunto = Column(Text, nullable=False)
    data_hora_realizacao = Column(DateTime, nullable=False)
    matricula = Column(String(20), ForeignKey("Usuario.matricula", ondelete="CASCADE"), nullable=False)
    tipo_atividade = Column(SAEnum(TipoAtividade, native_enum=True), nullable=False)
    data_hora_cadastro = Column(DateTime, server_default=func.now(), nullable=False)
    forma_aplicacao = Column(SAEnum(FormaAplicacao, native_enum=True), nullable=False)
    links_material = Column(Text, nullable=True)
    permite_consulta = Column(Boolean, nullable=False, default=False)
    pontuacao = Column(DECIMAL(5, 2), nullable=True)
    local_prova = Column(SAEnum(LocalProva, native_enum=True), nullable=False)
    materiais_necessarios = Column(Text, nullable=True)
    outros_materiais = Column(Text, nullable=True)
    avaliativa = Column(Boolean, nullable=False, default=False)
    turma = Column(SAEnum(Turma, native_enum=True), nullable=False)

    usuario = relationship("Usuario", back_populates="atividades")

class Evento(Base):
    __tablename__ = "Evento"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=True)
    data_inicio = Column(DateTime, nullable=False)
    data_fim = Column(DateTime, nullable=False)

    programacoes = relationship("ProgramacaoEvento", back_populates="evento", cascade="all, delete-orphan")
    participacoes = relationship("ParticipacaoEvento", back_populates="evento", cascade="all, delete-orphan")


class ProgramacaoEvento(Base):
    __tablename__ = "ProgramacaoEvento"

    id = Column(Integer, primary_key=True, autoincrement=True)
    evento_id = Column(Integer, ForeignKey("Evento.id", ondelete="CASCADE"), nullable=False)
    horario_inicio = Column(DateTime, nullable=False)
    horario_fim = Column(DateTime, nullable=False)
    tema = Column(String(255), nullable=False)
    organizador = Column(String(100), nullable=True)
    descricao = Column(Text, nullable=True)

    evento = relationship("Evento", back_populates="programacoes")


class ParticipacaoEvento(Base):
    __tablename__ = "ParticipacaoEvento"

    id = Column(Integer, primary_key=True, autoincrement=True)
    evento_id = Column(Integer, ForeignKey("Evento.id", ondelete="CASCADE"), nullable=False)
    usuario_id = Column(String(20), ForeignKey("Usuario.matricula", ondelete="CASCADE"), nullable=False)
    papel = Column(String(100))  # Ex: 'Organizador', 'Participante'

    evento = relationship("Evento", back_populates="participacoes")
