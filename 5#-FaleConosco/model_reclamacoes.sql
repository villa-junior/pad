-- Tabela base: Usuario
CREATE TABLE Usuario (
    matricula TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    senha TEXT NOT NULL
);
-- Tabela de Tópicos (simula ENUM)
CREATE TABLE Topicos (
    id_topico INTEGER PRIMARY KEY,
    nome TEXT NOT NULL UNIQUE
);

-- Inserção dos tópicos fixos
INSERT INTO Topicos (id_topico, nome) VALUES
(1, 'CALENDARIO'),
(2, 'CADASTRO'),
(3, 'AVALIACOES'),
(4, 'OUTROS');

-- Tabela Reclamacao
CREATE TABLE Reclamacao (
    id_reclamacao INTEGER PRIMARY KEY AUTOINCREMENT,
    matricula TEXT NOT NULL,
    id_topico INTEGER NOT NULL,
    descricao TEXT NOT NULL,
    data_reclamacao TEXT NOT NULL,
    FOREIGN KEY (matricula) REFERENCES Usuario(matricula),
    FOREIGN KEY (id_topico) REFERENCES Topicos(id_topico)
);
