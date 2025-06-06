# Automatizador de Importação de Dados do SUAP

## Descrição

Esta aplicação automatiza a importação e o tratamento de dados necessários para o pleno funcionamento de sistemas acadêmicos integrados. O sistema acessa as informações na plataforma SUAP, realiza o processamento adequado e armazena os dados em um banco de dados, tornando-os disponíveis para utilização por outros sistemas.

Os dados processados incluem:

- Perfis de usuários: professores e estudantes.
- Informações sobre disciplinas.

Com esta automação, evita-se o trabalho manual e garante-se maior integridade, consistência e atualização das informações.

## Funcionalidades

- Acesso automatizado à plataforma SUAP.
- Processamento e filtragem dos dados coletados.
- Inserção automatizada no banco de dados.
- Exibição dos dados em templates web.

## Pré-requisitos

- Python 3.8 ou superior.
- Conta de acesso válida na plataforma SUAP.
- Banco de dados configurado para recebimento das informações.

## Instalação

1. Crie um ambiente virtual e ative:

```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Crie um arquivo .env na raiz do projeto com as credenciais de acesso ao SUAP:

```env
MATRICULA=seu_usuario_suap
PASSWORD=sua_senha_suap
```
4. Configure o banco de dados:

Crie o arquivo do banco SQLite:

```bash
touch test.db  # Linux/MacOS
type nul > test.db  # Windows
```
5. Execute o script de criação das tabelas:

```bash
sqlite3 test.db < model_importacoes.sql
```
Certifique-se de ter o SQLite instalado em sua máquina. Caso não tenha, consulte: https://www.sqlite.org/download.html

⚠️ Importante: Não compartilhe nem versiona este arquivo, pois ele contém informações sensíveis.

Como executar
Execute o script principal para iniciar o processo de importação e tratamento dos dados:

```bash
python main.py
```
## A aplicação irá:

- Conectar-se à API do SUAP com as credenciais informadas.

- Coletar os dados necessários.

- Processar e filtrar as informações.

- Inserir os dados tratados no banco de dados.

