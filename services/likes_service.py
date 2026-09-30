from typing import Sequence

from sqlalchemy import select, delete, ScalarResult
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import Likes


def create_like(session: Session, user_id: int, track_id: int) -> Likes:
    like = Likes(user_id=user_id, track_id=track_id)
    session.add(like)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("Like already exists")
    session.refresh(like)
    return like

def delete_like(session: Session, user_id: int, track_id: int):
    result = session.execute(delete(Likes).where(
        Likes.user_id == user_id,
        Likes.track_id == track_id)
    )
    session.commit()
    return result.rowcount > 0

def get_likes_user(session: Session, user_id: int) -> Sequence[Likes]:
    return session.execute(select(Likes).where(Likes.user_id == user_id)).scalars().all()

def get_likes_track(session: Session, track_id: int, user_id: int) -> bool:
    result = session.execute(select(Likes).where(
        Likes.track_id == track_id,
        Likes.user_id == user_id)
    )
    return result.rowcount > 0

# todo (s) посмотреть что надо (апдейт вроде не нужен же?)

