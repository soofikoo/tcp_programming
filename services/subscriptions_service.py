from typing import Sequence

from sqlalchemy import delete, select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import Subscriptions


def create_subscription(session: Session, subscription_id: int, artist_id: int) -> Subscriptions:
    subscription = Subscriptions(
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
        delete(Subscriptions)
        .where(Subscriptions.subscription_id == subscription_id, Subscriptions.artist_id == artist_id)
    )
    session.commit()
    return result.rowcount > 0

def get_all_subscriptions_by_user(session: Session, user_id: int) -> Sequence[Subscriptions]:
    return session.execute(select(Subscriptions).where(Subscriptions.subscription_id == user_id)).scalars().all()

def get_all_subscriptions_by_artist(session: Session, artist_id: int) -> Sequence[Subscriptions]:
    return session.execute(select(Subscriptions).where(Subscriptions.artist_id == artist_id)).scalars().all()

def count_subscriptions_by_artist(session: Session, artist_id: int) -> int:
    return session.execute(select(func.count(Subscriptions.artist_id)).where(Subscriptions.artist_id == artist_id)).scalar_one()