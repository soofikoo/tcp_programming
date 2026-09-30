from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

'''
Создаем в engine и sessionmaker в одном месте проекта

Пример использования:

from database import Session
with Session() as session:
    genre = create_genre(session, "rock")
'''

# TODO (К) в секреты
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/music"

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)