from typing import Sequence

from sqlalchemy import delete, select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import Subscription


def create_subscription(session: Session, subscription_id: int, artist_id: int) -> Subscription:
    subscription = Subscription(
        subscription_id = subscription_id,
        artist_id = artist_id,
    )
    session.add(subscription)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("Subscription already exists")
    session.refresh(subscription)
    return subscription

def delete_subscription(session: Session, subscription_id: int, artist_id: int) -> bool:
    result = session.execute(
        delete(Subscription)
        .where(Subscription.subscription_id == subscription_id, Subscription.artist_id == artist_id)
    )
    session.commit()
    return result.rowcount > 0

def count_Subscription_by_artist(session: Session, artist_id: int) -> int:
    return session.execute(select(func.count(Subscription.artist_id)).where(Subscription.artist_id == artist_id)).scalar_one()

#todo (s)
def get_Subscription_by_user(session: Session, user_id: int) -> Sequence[Subscription]:
    pass