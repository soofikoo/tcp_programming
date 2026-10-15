from typing import Sequence

from sqlalchemy import update, select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import Genre


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
    try:
        session.execute(update(Genre).where(Genre.id == genre_id).values(name=name))
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("Genre already exists")
    return get_genre(session, genre_id)


def get_genre(session: Session, genre_id: int) -> Genre | None:
    return session.get(Genre, genre_id)


def get_genres(session: Session) -> Sequence[Genre]:
    return session.execute(select(Genre).order_by(Genre.name)).scalars().all()


def delete_genre(session: Session, genre_id: int) -> bool:
    result = session.execute(delete(Genre).where(Genre.id == genre_id))
    session.commit()
    return result.rowcount > 0
