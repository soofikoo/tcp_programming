from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
'''
Создаем в engine и sessionmaker в одном месте проекта

Пример использования:

from database import Session
with Session() as session:
    genre = create_genre(session, "rock")
'''

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)