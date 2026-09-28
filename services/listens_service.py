from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.listens_model import Listens
from models.tracks_model import Track


def create_listen(session: Session, user_id: int, track_id: int) -> Listens:
    listen = Listens(user_id=user_id, track_id=track_id)
    session.add(listen)
    session.execute(
        update(Track).where(Track.id == track_id).values(play_count=Track.play_count + 1)
    )
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("User or track not found")
    session.refresh(listen)
    return listen