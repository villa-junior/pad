import requests
from bs4 import BeautifulSoup
import re
from typing import List
from dotenv import load_dotenv
import os
from models import Disciplina,Professor,Estudante

load_dotenv()

session = requests.Session()

# URLs
LOGIN_URL = 'https://suap.ifba.edu.br/accounts/login/?next=/'
DISCIPLINAS_URL = 'https://suap.ifba.edu.br/edu/salas_virtuais/'
BASE_URL = 'https://suap.ifba.edu.br'

# Credenciais
username = os.getenv('MATRICULA')
password = os.getenv('PASSWORD')

# Headers
headers = {
    'Referer': LOGIN_URL,
    'User-Agent': 'Mozilla/5.0'
}

def login():
    login_page = session.get(LOGIN_URL, headers=headers)
    soup = BeautifulSoup(login_page.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'}).get('value')

    payload = {
        'username': username,
        'password': password,
        'csrfmiddlewaretoken': csrf_token
    }
    #print(payload)
    response = session.post(LOGIN_URL, data=payload, headers=headers)

    if response.ok and 'logout' in response.text.lower():
        print('Login realizado com sucesso.')
        return True
    else:
        print('Falha no login.')
        return False

def extrair_disciplinas() -> List[Disciplina]:
    disciplinas: List[Disciplina] = []

    response = session.get(DISCIPLINAS_URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    tbodies = soup.find_all('tbody')

    for tbody in tbodies:
        for row in tbody.find_all('tr'):
            tds = row.find_all('td')
            if len(tds) >= 4:
                sigla = tds[0].get_text(strip=True)
                nome = tds[1].get_text(strip=True)

                link = tds[3].find('a')
                href = link['href'] if link else ''

                disciplinas.append(Disciplina(sigla=sigla, nome=nome, href=href))

    return disciplinas

def extrair_professores(disciplina:Disciplina) -> List[Professor]:
    url = BASE_URL+disciplina.href+"?tab=dados_gerais"
    
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    professores:List[Professor] = []

    for box in soup.find_all('div', class_='box-info'):
        nome_tag = box.find('h4')
        nome = nome_tag.get_text(strip=True) if nome_tag else None

        matricula = None
        for dt in box.find_all('dt'):
            if dt.get_text(strip=True) == 'Matrícula:':
                dd = dt.find_next_sibling('dd')
                if dd:
                    matricula = dd.get_text(strip=True)
                break  # Encontrou a matrícula, pode parar

        if nome and matricula:
            professores.append(Professor(matricula=matricula,nome=nome))

    return professores

def extrair_estudantes(disciplina: Disciplina) -> List[Estudante]:
    url = BASE_URL + disciplina.href + "?tab=participantes"
    
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    estudantes: List[Estudante] = []

    cards = soup.find_all('div', class_='card')

    for card in cards:
        # Pega o nome
        nome_tag = card.find('h4')
        nome = nome_tag.get_text(strip=True) if nome_tag else None

        # Pega a matrícula
        matricula = None
        for dt in card.find_all('dt'):
            if dt.get_text(strip=True) == 'Matrícula:':
                dd = dt.find_next_sibling('dd')
                if dd:
                    matricula = dd.get_text(strip=True)
                break  # achou a matrícula, pode parar

        if nome and matricula:
            estudante = Estudante(nome=nome, matricula=matricula)
            estudantes.append(estudante)

    return estudantes

def get_data() -> List[Disciplina]:
    if login():
        print("Coletando dados do suap....")
        disciplinas = extrair_disciplinas()
        for d in disciplinas:
            d.setProfessores(professores=extrair_professores(disciplina=d))
            d.setEstudantes(estudantes=extrair_estudantes(disciplina=d))
    return disciplinas        
        
       

