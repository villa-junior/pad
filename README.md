# Sistema de Gerenciamento Acadêmico - PPA

---

## Descrição

Este é um sistema de gerenciamento acadêmico projetado para auxiliar docentes e administradores no registro, acompanhamento e gerenciamento de atividades acadêmicas. A aplicação é modular, permitindo a fácil expansão e manutenção de funcionalidades.

As principais funcionalidades incluem:

- **Cadastro de Atividades:** Permite que docentes registrem suas atividades acadêmicas, como aulas, pesquisas e projetos de extensão.
- **Fale Conosco:** Um canal de comunicação para que os usuários possam enviar reclamações, sugestões e outras mensagens.
- **Autenticação de Usuários:** Sistema de login, registro e recuperação de senha.
- **Visualização de Calendário:** Uma interface para visualizar eventos e atividades em um calendário.

---

## Funcionalidades Detalhadas

### Cadastro de Atividades (`atividades.py`)

O módulo de atividades permite o registro e a visualização de atividades acadêmicas. Os usuários podem:

- Inserir novas atividades através de um formulário.
- Visualizar uma lista de atividades já cadastradas.
- Editar e excluir atividades existentes.

### Fale Conosco (`faleConosco.py`)

Este módulo oferece um canal de comunicação direto com a administração do sistema. Os usuários podem:

- Enviar mensagens, reclamações ou sugestões através de um formulário.
- A administração pode visualizar e gerenciar as mensagens recebidas.

### Fórum (`forum.py`)

O módulo de fórum permite a postagem e visualização de posts num fórum comapartilhados

- Enviar novos posts através de um formulário.
- Editar e excluir seus posts existentes.
- Visualizar uma lista de posts já cadastradas.

---

## Estrutura do Projeto e Modularização em Python

O projeto utiliza uma estrutura modular para organizar o código de forma clara e eficiente. Cada funcionalidade principal é separada em seu próprio arquivo Python (módulo), o que oferece os seguintes benefícios:

- **Organização:** O código é mais fácil de encontrar e entender.
- **Manutenção:** Alterações em uma funcionalidade não afetam outras partes do sistema.
- **Reutilização:** Módulos podem ser reutilizados em outras partes da aplicação.
- **Escalabilidade:** Novas funcionalidades podem ser adicionadas como novos módulos sem a necessidade de alterar o código existente.

A estrutura de diretórios `codigo/` contém os principais módulos da aplicação, como `atividades.py`, `faleConosco.py`, `auth.py`,`forum.py` e `calendario.py`. O arquivo `main.py` é o ponto de entrada da aplicação, que importa e inicializa os outros módulos.

---

## Banco de Dados e Migrações com Flask-Migrate

O sistema utiliza o Flask-Migrate para gerenciar as migrações do banco de dados. Isso permite que a estrutura do banco de dados evolua junto com o código da aplicação de forma controlada e versionada.

### Models (`models.py`)

O arquivo `models.py` define a estrutura das tabelas do banco de dados utilizando o SQLAlchemy. As principais tabelas são:

- `User`: Armazena as informações dos usuários.
- `Atividade`: Armazena os detalhes das atividades cadastradas.
- `Reclamacao`: Armazena as mensagens enviadas através do formulário "Fale Conosco".
- `PostForum`: Armazena os posts enviados no fórum
### Comandos do Flask-Migrate

Para criar as tabelas e gerenciar as migrações, utilize os seguintes comandos:

1.  **Inicializar o ambiente de migração (apenas na primeira vez):**
    ```bash
    cd codigo
    flask db init
    ```

2.  **Criar uma nova migração após alterações nos models:**
    ```bash
    flask db migrate -m "Descrição da migração"
    ```

3.  **Aplicar a migração ao banco de dados:**
    ```bash
    flask db upgrade
    ```

---

## Pré-requisitos

- Python 3.8 ou superior.
- MySQL ou outro banco de dados relacional compatível com SQLAlchemy.
- Um ambiente virtual Python.

---

## Instalação

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-repositorio>
    cd <nome-do-diretorio>
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/macOS
    .venv\Scripts\activate    # Windows
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis:
    ```
    DATABASE_URL="mysql+pymysql://user:password@host/database"
    FLASK_APP=.:create_app
    SECRET_KEY=java_e_muito_melhor
    EMAIL=comunicao.pad@gmail.com
    SENHA_APP=uckpdielazujhfdg
    ```

5.  **Execute as migrações do banco de dados:**
    ```bash
    flask db upgrade
    ```

---

## Como Executar

Para iniciar a aplicação, execute o seguinte comando:

```bash
python pad.py # via arquivo
cd codigo && flask run # via módulo flask
```

Acesse a aplicação em seu navegador no endereço [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## Observações

- Certifique-se de que o serviço do seu banco de dados esteja em execução antes de iniciar a aplicação.
- As credenciais no arquivo `.env` são essenciais para o funcionamento do banco de dados e do sistema de e-mails.