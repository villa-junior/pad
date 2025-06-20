# 📝 PAD



## 🚀 Como rodar o projeto

1. **Crie e ative o ambiente virtual**:
   ```bash
   py -m venv venv
   venv\Scripts\activate

2. **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    Se não funcionar instale manualmente o flask, sqlalchemy e o dotenv

3. **.env:**
    ```bash
    É necessário um arquivo .env na pasta do projeto
    jogue esse trecho nele
    DATABASE_URL=mysql+pymysql://root:<senha_super_díficil>@<endereço_db>:3306/bancopad
    lembre de mudar a senha super dificil e o endereço do db

