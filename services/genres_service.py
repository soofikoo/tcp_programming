from sqlalchemy import update, select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.genres_model import Genres


def create_genre(session: Session, name: str) -> Genres:
    genre = Genres(name=name)
    session.add(genre)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("Genre already exists")
    session.refresh(genre)
    return genre

def update_genre(session: Session, genre_id: int, name: str) -> Genres | None:
    session.execute(update(Genres).where(Genres.id == genre_id).values(name=name))
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("Genre already exists")
    return get_genre(session=session, genre_id=genre_id)
# todo (k) зачем гет, если это апдейт

def get_genre(session: Session, genre_id: int) -> Genres | None:
    return session.execute(select(Genres).where(Genres.id == genre_id)).scalar_one_or_none()

def delete_genre(session: Session, genre_id: int) -> bool:
    result = session.execute(delete(Genres).where(Genres.id == genre_id))
    session.commit()
    return result.rowcount > 0

# todo (s) посмотреть что нужно еще