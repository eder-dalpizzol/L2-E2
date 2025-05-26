 Escolinha Scheduling System

Teste de versao live:
https://dalpizzol.pythonanywhere.com/

## Descrição
Aplicação Flask para visualizar:
- Horas de aula por professor  
- Horários ocupados e livres das salas

## Tecnologias
- Python 3.x  
- Flask  
- SQLite  
- SQLAlchemy  
- Bootstrap (via CDN nos templates)



## Instalação
1. Clone o repositório  
2. Crie e ative um ambiente virtual:

   python3 -m venv venv
   source venv/bin/activate

    Instale dependências:

    pip install flask flask_sqlalchemy

População de dados

Logo após a primeira execução do app.py, o banco horarios.db será criado e populado automaticamente com dados de exemplo.


Execução

python app.py

Acesse no navegador:

    http://localhost:5000/ → página inicial

    http://localhost:5000/horas_por_professor

    http://localhost:5000/salas_horarios
