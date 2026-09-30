from sqlalchemy import update, select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.genre_model import Genre


def create_genre(session: Session, name: str) -> Genre:
    genre = Genre(name=name)
    session.add(genre)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("Genre already exists")
    session.refresh(genre)
    return genre

def update_genre(session: Session, genre_id: int, name: str) -> Genre | None:
    session.execute(update(Genre).where(Genre.id == genre_id).values(name=name))
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("Genre already exists")
    return get_genre(session=session, genre_id=genre_id)
# todo (k) зачем гет, если это апдейт

def get_genre(session: Session, genre_id: int) -> Genre | None:
    return session.execute(select(Genre).where(Genre.id == genre_id)).scalar_one_or_none()

def delete_genre(session: Session, genre_id: int) -> bool:
    result = session.execute(delete(Genre).where(Genre.id == genre_id))
    session.commit()
    return result.rowcount > 0