from sqlalchemy import update, select, delete, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import Album, Artist, Like, Listen, Subscription, Track


def create_artist(session: Session, artist_id: int, bio: str | None = None) -> Artist:
    artist = Artist(artist_id=artist_id, bio=bio)
    session.add(artist)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("Artist already exists")
    return artist


def update_artist(session: Session, artist_id: int, bio: str | None) -> Artist | None:
    session.execute(update(Artist).where(Artist.artist_id == artist_id).values(bio=bio))
    session.commit()
    return get_artist(session, artist_id)


def get_artist(session: Session, artist_id: int) -> Artist | None:
    return session.get(Artist, artist_id)


def delete_artist(session: Session, artist_id: int) -> bool:
    result = session.execute(delete(Artist).where(Artist.artist_id == artist_id))
    session.commit()
    return result.rowcount > 0


def get_artist_albums(session: Session, artist_id: int) -> list[Album]:
    return list(session.execute(
        select(Album).where(Album.artist_id == artist_id).order_by(Album.release_date.desc())
    ).scalars().all())


def get_artist_stats(session: Session, artist_id: int) -> dict:
    artist_tracks = select(Track.id).where(Track.artist_id == artist_id)
    return {
        "tracks": session.scalar(select(func.count()).select_from(artist_tracks.subquery())),
        "listens": session.scalar(select(func.count(Listen.id)).where(Listen.track_id.in_(artist_tracks))),
        "likes": session.scalar(select(func.count()).select_from(Like).where(Like.track_id.in_(artist_tracks))),
        "subscribers": session.scalar(
            select(func.count()).select_from(Subscription).where(Subscription.artist_id == artist_id)),
    }
