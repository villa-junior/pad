from typing import List

class Professor():
    def __init__(self,matricula,nome):
        self.matricula = matricula
        self.nome = nome
    
    def __str__(self):
        return f"Professor(matricula={self.matricula}, nome={self.nome})"

class Estudante():
    def __init__(self,matricula,nome):
        self.matricula = matricula
        self.nome = nome

    def __str__(self):
        return f"Estudantes(matricula={self.matricula}, nome={self.nome})"

class Disciplina():
    def __init__(self, sigla, nome, href):
        self.sigla = sigla
        self.nome = nome
        self.href = href
        self.professores = []
        self.estudantes = []

        self.setDisciplinaId(href=href)
        
    def setDisciplinaId(self,href):
        self.id_disciplina = href.strip("/").split("/")[-1]

    def setProfessores(self, professores: List['Professor']):
        self.professores = professores
    
    def setEstudantes(self, estudantes: List['Estudante']):
        self.estudantes = estudantes

    def __str__(self):
        profs = '\n    '.join(str(p) for p in self.professores) if self.professores else "Nenhum"
        ests = '\n    '.join(str(e) for e in self.estudantes) if self.estudantes else "Nenhum"
        
        return (
            f"DISCIPLINA:\n"
            f"  Sigla: {self.sigla}\n"
            f"  Nome: {self.nome}\n"
            f"  Link: {self.href}\n"
            f"  Professores:\n    {profs}\n"
            f"  Estudantes:\n    {ests}\n"
        )

