from datetime import date
from typing import Sequence

from sqlalchemy import update, select, delete, Row
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import Track, User, TrackGenre


def create_track(session: Session, title: str, album_id: int, duration: int,
                 file_path: str, release_date: date, artist_id: int) -> Track:
    track = Track(title=title, album_id=album_id, duration=duration,
                  file_path=file_path, release_date=release_date, artist_id=artist_id)
    session.add(track)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise
    session.refresh(track)
    return track


def update_track(session: Session, track_id: int, title: str, album_id: int | None) -> Track | None:
    try:
        session.execute(update(Track).where(Track.id == track_id).values(title=title, album_id=album_id))
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("Album not found")
    return get_track(session, track_id)


def delete_track(session: Session, track_id: int) -> bool:
    result = session.execute(delete(Track).where(Track.id == track_id))
    session.commit()
    return result.rowcount > 0


def get_track(session: Session, track_id: int) -> Track | None:
    return session.get(Track, track_id)


_TRACK_ROW = (Track.id, Track.title, Track.duration, Track.file_path, User.username.label("artist_name"))


def get_track_player(session: Session, track_id: int) -> Row | None:
    return session.execute(
        select(*_TRACK_ROW)
        .join(User, User.id == Track.artist_id)
        .where(Track.id == track_id)
    ).one_or_none()


def get_tracks(session: Session) -> Sequence[Row]:
    return session.execute(
        select(*_TRACK_ROW).join(User, User.id == Track.artist_id).order_by(Track.id)
    ).all()


def get_track_list_by_genre(session: Session, genre_ids: list[int]) -> Sequence[Row]:
    return session.execute(
        select(*_TRACK_ROW)
        .join(User, User.id == Track.artist_id)
        .join(TrackGenre, TrackGenre.track_id == Track.id)
        .where(TrackGenre.genre_id.in_(genre_ids))
        .distinct()
        .order_by(Track.id)
    ).all()
