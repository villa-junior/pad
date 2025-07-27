-- Tabela base: Usuario (por enquanto manter genérico)
CREATE TABLE IF NOT EXISTS Usuario (
    matricula VARCHAR(20) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL
);

-- Provavelmente vai precisar de mudanças
CREATE TABLE IF NOT EXISTS Atividade (
    id INT AUTO_INCREMENT PRIMARY KEY,
    materia VARCHAR(255) NOT NULL,
    assunto TEXT NOT NULL,
    data_hora_realizacao DATETIME NOT NULL,
    matricula VARCHAR(20) NOT NULL,
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
    FOREIGN KEY (matricula) REFERENCES Usuario(matricula) ON DELETE CASCADE
);

-- Falta implementar
CREATE TABLE IF NOT EXISTS Notificacao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    atividade_id INT NOT NULL,
    mensagem TEXT NOT NULL,
    data_hora_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (atividade_id) REFERENCES Atividade(id) ON DELETE CASCADE
);
-- Tabela Reclamacao
CREATE TABLE IF NOT EXISTS Reclamacao (
    id_reclamacao INT AUTO_INCREMENT PRIMARY KEY,   
    matricula VARCHAR(20) NOT NULL,
    topico ENUM('Calendário', 'Cadastro de Perfil', 'Cadastro de Atividades', 'Avaliações','Outros') NOT NULL,
    descricao TEXT NOT NULL,
    data_reclamacao DATETIME NOT NULL,
    FOREIGN KEY (matricula) REFERENCES Usuario(matricula)
);
--Tabela Evento 
CREATE TABLE IF NOT EXISTS Evento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL
);
--Tabela Programação do Evento
CREATE TABLE IF NOT EXISTS ProgramacaoEvento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    evento_id INT NOT NULL,
    horario_inicio DATETIME NOT NULL,
    horario_fim DATETIME NOT NULL,
    tema VARCHAR(255),
    organizador VARCHAR(100),
    local VARCHAR(100),
    descricao TEXT,
    FOREIGN KEY (evento_id) REFERENCES Evento(id) ON DELETE CASCADE
);
--Tabela Participação do Evento
CREATE TABLE IF NOT EXISTS ParticipacaoEvento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    evento_id INT NOT NULL,
    matricula VARCHAR(20) NOT NULL,
    papel ENUM('Participante', 'Organizador', 'Palestrante') NOT NULL,
    FOREIGN KEY (evento_id) REFERENCES Evento(id) ON DELETE CASCADE,
    FOREIGN KEY (matricula) REFERENCES Usuario(matricula) ON DELETE CASCADE
);

