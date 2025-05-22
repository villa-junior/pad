create database bancopad;
USE bancopad;

-- Tabela para testes
CREATE TABLE IF NOT EXISTS Docente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

-- Provavelmente vai precisar de mudanças
CREATE TABLE IF NOT EXISTS Atividade (
    id INT AUTO_INCREMENT PRIMARY KEY,
    materia VARCHAR(255) NOT NULL,
    assunto TEXT NOT NULL,
    data_hora_realizacao DATETIME NOT NULL,
    docente_id INT NOT NULL,
    tipo_atividade ENUM('Prova Objetiva', 'Prova Discursiva', 'Prova Mista', 'Seminário', 'Lista de Atividades') NOT NULL,
    data_hora_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    forma_aplicacao ENUM('Individual', 'Em Dupla', 'Em Grupo') NOT NULL,
    links_material TEXT,
    permite_consulta BOOLEAN NOT NULL DEFAULT FALSE,
    pontuacao DECIMAL(5,2),
    local_prova ENUM('Sala de Aula', 'Laboratório', 'AVA', 'Ginásio') NOT NULL,
    materiais_necessarios TEXT,
    outros_materiais TEXT NULL,
    avaliativa BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (docente_id) REFERENCES Docente(id) ON DELETE CASCADE
);


-- Falta implementar
CREATE TABLE IF NOT EXISTS Notificacao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    atividade_id INT NOT NULL,
    mensagem TEXT NOT NULL,
    data_hora_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (atividade_id) REFERENCES Atividade(id) ON DELETE CASCADE
);






