from sqlalchemy import update, select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.artist_profiles_model import Artist


def create_artist(session: Session, artist_id: int, bio: str) -> Artist:
    artist = Artist(artist_id=artist_id, bio=bio)
    session.add(artist)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("Artist already exists")
    return artist

def update_artist(session: Session, artist_id: int, bio: str) -> Artist | None:
    session.execute(update(Artist).where(Artist.artist_id == artist_id).values(bio=bio))
    session.commit()

def get_artist(session: Session, artist_id: int) -> Artist | None:
    return session.execute(select(Artist).where(Artist.artist_id == artist_id)).scalar_one_or_none()

def delete_artist(session: Session, artist_id: int) -> bool:
    result = session.execute(delete(Artist).where(Artist.artist_id == artist_id))
    return result.rowcount > 0


# todo (s) посмотреть с Кириллом нужен ли здесь еще гет, нужен, надо подсосать имя артиста из юзера