from datetime import datetime

from sqlalchemy import update, select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import Track


def create_track(session: Session, title: str, album_id: int, duration: int, file_path: str, upload_date: datetime, artist_id: int) -> Track:
    track = Track(title=title, album_id=album_id, duration=duration, file_path=file_path, upload_date=upload_date, artist_id=artist_id)
    session.add(track)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("Track already exists")
    return track

def update_track(session: Session, track_id: int, title: str) -> None:
    session.execute(update(Track).where(Track.id == track_id).values(title=title))
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("Track already exists")

def delete_track(session: Session, track_id: int) -> bool:
    result = session.execute(delete(Track).where(Track.id == track_id))
    return result.rowcount > 0

def get_track(session: Session, track_id: int) -> Track | None:
    return session.execute(select(Track).where(Track.id == track_id)).scalar_one_or_none()

# todo (s) посмотреть, нужно ли что-то еще