from typing import Sequence

from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import Listen


def create_listen(session: Session, user_id: int, track_id: int) -> Listen:
    listen = Listen(user_id=user_id, track_id=track_id)
    session.add(listen)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("User or track not found")
    session.refresh(listen)
    return listen


def get_listen(session: Session, listen_id: int) -> Listen | None:
    return session.get(Listen, listen_id)


def get_user_listens(session: Session, user_id: int) -> Sequence[Listen]:
    return session.execute(
        select(Listen).where(Listen.user_id == user_id).order_by(Listen.created_at.desc())
    ).scalars().all()


def count_track_listens(session: Session, track_id: int) -> int:
    return session.execute(select(func.count(Listen.id)).where(Listen.track_id == track_id)).scalar_one()
