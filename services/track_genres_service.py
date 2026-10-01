from typing import Sequence

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import TrackGenre


def create_track_genre(session: Session, track_id: int, genre_id) -> TrackGenre:
    track = TrackGenre(track_id = track_id, genre_id = genre_id)
    session.add(track)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("Track genre already exists")
    return track

def delete_track_genre(session: Session, track_id: int, genre_id: int) -> bool:
    result = session.execute(delete(TrackGenre).where(
        TrackGenre.track_id == track_id,
        TrackGenre.genre_id == genre_id)
    )
    session.commit()
    return result.rowcount > 0

def get_track_genres(session: Session, track_id: int) -> Sequence[TrackGenre]:
    return session.execute(select(TrackGenre).where(TrackGenre.track_id == track_id)).scalars().all()
