CREATE TABLE Disciplina (
    disciplina_id INT PRIMARY KEY,
    sigla VARCHAR(10) NOT NULL,
    nome VARCHAR(100) NOT NULL
);

CREATE TABLE Professor (
    matricula_professor INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

CREATE TABLE Estudante (
    matricula_estudante INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- Tabela de relacionamento N:N entre Professor e Disciplina
CREATE TABLE Professor_Disciplina (
    matricula_professor INT,
    disciplina_id INT,
    PRIMARY KEY (matricula_professor, disciplina_id),
    FOREIGN KEY (matricula_professor) REFERENCES Professor(matricula_professor),
    FOREIGN KEY (disciplina_id) REFERENCES Disciplina(disciplina_id)
);

-- Tabela de relacionamento N:N entre Estudante e Disciplina
CREATE TABLE Estudante_Disciplina (
    matricula_estudante INT,
    disciplina_id INT,
    PRIMARY KEY (matricula_estudante, disciplina_id),
    FOREIGN KEY (matricula_estudante) REFERENCES Estudante(matricula_estudante),
    FOREIGN KEY (disciplina_id) REFERENCES Disciplina(disciplina_id)
);

