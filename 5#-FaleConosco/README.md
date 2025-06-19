# Sistema de Coleta de Feedbacks

## Descrição

Esta aplicação foi desenvolvida para garantir a adequada manutenção e o contínuo aperfeiçoamento de sistemas acadêmicos integrados, oferecendo uma plataforma estruturada para a coleta de feedback dos usuários. 

O sistema disponibiliza um formulário no qual os usuários podem registrar:

- Reclamações
- Sugestões
- Observações

Cada feedback é vinculado a um tópico específico. A aplicação autentica o usuário antes do registro, garantindo a integridade e a segurança das informações coletadas. Os dados são armazenados no banco de dados, possibilitando consulta e análise pelos técnicos responsáveis pela manutenção e evolução da aplicação.

## Funcionalidades

- Formulário web para registro de feedbacks.
- Autenticação de usuários.
- Armazenamento seguro das informações no banco de dados.
- Consulta dos registros por técnicos responsáveis.

## Pré-requisitos

- Python 3.8 ou superior.
- Banco de dados SQLite.
- Ferramenta para execução de scripts SQL (opcional, para configuração inicial).

## Instalação

1. Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure o banco de dados:

Crie o arquivo do banco SQLite:

```bash
touch test.db  # Linux/MacOS
type nul > test.db  # Windows
```
Execute o script de criação das tabelas:

```bash
sqlite3 test.db < model_reclamacoes.sql
```
Certifique-se de ter o SQLite instalado em sua máquina. Caso não tenha, consulte: https://www.sqlite.org/download.html


### Como executar
Execute o script principal para iniciar o processo de importação e tratamento dos dados:

```bash
python main.py
```
## A aplicação irá:

- Conectar-se à API do SUAP com as credenciais informadas.

- Coletar os dados necessários.

- Processar e filtrar as informações.

- Inserir os dados tratados no banco de dados.
