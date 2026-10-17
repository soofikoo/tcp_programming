from typing import Sequence

from sqlalchemy import delete, select, func, Row
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import Subscription, User


def create_subscription(session: Session, subscriber_id: int, artist_id: int) -> Subscription:
    subscription = Subscription(subscriber_id=subscriber_id, artist_id=artist_id)
    session.add(subscription)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("Subscription already exists")
    session.refresh(subscription)
    return subscription


def delete_subscription(session: Session, subscriber_id: int, artist_id: int) -> bool:
    result = session.execute(
        delete(Subscription)
        .where(Subscription.subscriber_id == subscriber_id, Subscription.artist_id == artist_id)
    )
    session.commit()
    return result.rowcount > 0


def count_subscription_by_artist(session: Session, artist_id: int) -> int:
    return session.execute(
        select(func.count()).select_from(Subscription).where(Subscription.artist_id == artist_id)
    ).scalar_one()


def get_subscription_by_user(session: Session, subscriber_id: int) -> Sequence[Row]:
    return session.execute(
        select(Subscription.artist_id, User.username.label("artist_name"), Subscription.subscribed_at)
        .join(User, User.id == Subscription.artist_id)
        .where(Subscription.subscriber_id == subscriber_id)
        .order_by(User.username)
    ).all()