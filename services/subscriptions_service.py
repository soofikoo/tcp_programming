from typing import Sequence, Any

from sqlalchemy import delete, select, func, Row
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql._typing import _TP

from models import Subscription, User


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

def count_subscription_by_artist(session: Session, artist_id: int) -> int:
    return session.execute(select(func.count(Subscription.artist_id)).where(Subscription.artist_id == artist_id)).scalar_one()

def get_subscription_by_user(session: Session, subscription_id: int) -> Sequence[Row[Any]]:
    return session.execute(
        select(User.username.label("artist_name"), Subscription.subscribed_at)
        .join(Subscription, User.id == Subscription.artist_id)
        .where(Subscription.subscription_id == subscription_id)
        .order_by(User.username)
    ).all()