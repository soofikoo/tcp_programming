from datetime import datetime

from sqlalchemy import update, select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import Album


def create_album(session: Session, title: str, artist_id: int, release_date: datetime, cover_url: str) -> Album:
    album = Album(title=title, artist_id=artist_id, release_date=release_date, cover_url=cover_url)
    session.add(album)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("Album already exists")
    return album

def update_album(session: Session, album_id: int, title: str, artist_id: int, release_date: datetime, cover_url: str) -> Album | None:
    session.execute(update(Album).where (Album.id == album_id).values(
        title=title, artist_id=artist_id, release_date=release_date, cover_url=cover_url
    ))
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("Album already exists")
    return get_album(session, album_id)

def delete_album(session: Session, album_id: int) -> bool:
    result = session.execute(delete(Album).where(Album.id == album_id))
    session.commit()
    return result.rowcount > 0

def get_album(session: Session, album_id: int) -> Album | None:
    return session.execute(select(Album).where(Album.id == album_id)).scalar_one_or_none()

#todo (s)
def get_album_by_track(session: Session, track_id: int) -> Album | None:
    pass
