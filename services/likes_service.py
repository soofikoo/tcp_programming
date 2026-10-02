from typing import Sequence

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import Like, Track, User


def create_like(session: Session, user_id: int, track_id: int) -> Like:
    like = Like(user_id=user_id, track_id=track_id)
    session.add(like)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("Like already exists")
    session.refresh(like)
    return like

def delete_like(session: Session, user_id: int, track_id: int):
    result = session.execute(delete(Like).where(
        Like.user_id == user_id,
        Like.track_id == track_id)
    )
    session.commit()
    return result.rowcount > 0

def get_likes_user(session: Session, user_id: int) -> Sequence[Like]:
    return session.execute(select(Like).where(Like.user_id == user_id)).scalars().all()

def is_like_track(session: Session, track_id: int, user_id: int) -> bool:
    return session.execute(
        select(Like).where(Like.track_id == track_id, Like.user_id == user_id)
    ).scalar_one_or_none() is not None

def get_liked_track(session: Session, user_id: int):
    return session.execute(select(Track.id, Track.title, Track.duration, User.username.label("artist_name"), Like.created_at)
                            .join(Track, Track.id == Like.track_id)
                            .join(User, User.id == Like.user_id)
                            .where(Like.user_id == user_id)
                            .order_by(Like.created_at.desc())
    ).all()

