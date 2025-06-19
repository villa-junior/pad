
# Cadastro de Atividades - PAD

---

## Descrição

Esta aplicação faz parte do sistema PAD e tem como objetivo permitir o cadastro e a visualização das atividades acadêmicas vinculadas a docentes, servindo como base para registro, acompanhamento e avaliação de desempenho.

A tela de Cadastro de Atividades permite:

- Inserir atividades realizadas por docentes.
- Visualizar atividades previamente registradas.
- Estruturar os dados para futuras etapas de análise e geração de relatórios.

As atividades são armazenadas em um banco de dados relacional e podem ser consultadas e atualizadas posteriormente por administradores do sistema.

---

## Funcionalidades

- Formulário para registro de atividades.
- Leitura de dados do banco para exibição dinâmica.
- Estruturação da tabela `atividade_pad` e vínculo com docente.
- Interface pronta para integração com login e validações futuras.

---

## Pré-requisitos

- Python 3.8 ou superior.
- Banco de dados MySQL.
- Script SQL fornecido para criar estrutura básica (`bancopad.sql`).
- Navegador para acessar o sistema via localhost.

---

## Instalação

1. Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate         # Windows
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure o banco de dados:

   - Certifique-se de que o MySQL está rodando.
   - Crie o banco e execute o script `bancopad.sql`.

   ```bash
   mysql -u root -p < bancopad.sql
   ```

4. Ajuste as credenciais de acesso ao banco no arquivo `atividadespad.py`.

---

## Como executar

```bash
python atividadespad.py
```

- Acesse em: [http://localhost:5000](http://localhost:5000)
- A tela de cadastro será exibida com os dados dos docentes carregados automaticamente.

---

## Observações

- O banco de dados precisa conter ao menos um docente registrado para que a página funcione corretamente.
- Alguns campos e validações estão em desenvolvimento.
