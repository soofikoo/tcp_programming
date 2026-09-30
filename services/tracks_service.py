from datetime import datetime
from typing import Sequence

from sqlalchemy import update, select, delete, Result, Row
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import Track, Album, User, TrackGenre


def create_track(session: Session, title: str, album_id: int | None, duration: int, file_path: str, upload_date: datetime, artist_id: int) -> Track:
    track = Track(title=title, album_id=album_id, duration=duration, file_path=file_path, upload_date=upload_date, artist_id=artist_id)
    session.add(track)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("Track already exists")
    session.refresh(track)
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
    session.commit()
    return result.rowcount > 0

def get_track(session: Session, track_id: int) -> Track | None:
    return session.execute(select(Track).where(Track.id == track_id)).scalar_one_or_none()

def get_track_player(session: Session, track_id: int) -> Row[tuple[int, str, int, str, str]] | None:
    return (session.execute(select(Track.id, Track.title, Track.duration, Track.file_path, User.username.label("artist_name"))
                            .join(User, User.id == Track.artist_id)
                            .where(Track.id == track_id))
            .one_or_none())

def get_track_list_by_genre(session: Session, genres_id: list[int]) -> Sequence[Row[tuple[int, str, int, str, str]]]:
    return (session.execute(select(Track.id, Track.title, Track.duration, Track.file_path, User.username.label("artist_name"))
                            .join(User, User.id == Track.artist_id)
                            .join(TrackGenre, TrackGenre.track_id == Track.id)
                            .where(TrackGenre.genre_id.in_(genres_id))
                            .distinct()
                            )
            ).all()