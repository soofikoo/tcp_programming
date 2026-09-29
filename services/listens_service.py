from typing import Any, Sequence

from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.listens_model import Listens


def create_listen(session: Session, user_id: int, track_id: int) -> Listens:
    listen = Listens(user_id=user_id, track_id=track_id)
    session.add(listen)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("User or track not found")
    session.refresh(listen)
    return listen

def get_listen(session: Session, listen_id: int) -> Listens:
    return session.execute(select(Listens).where(Listens.id == listen_id)).scalar_one_or_none()

def get_list_user_listens(session: Session, user_id: int) -> Sequence[Listens]:
    return session.execute(select(Listens).where(Listens.user_id == user_id)).scalars().all()

def count_track_listens(session: Session, track_id: int) -> int:
    return session.execute(
        select(func.count(Listens.id)).where(Listens.track_id == track_id)
    ).scalar_one()