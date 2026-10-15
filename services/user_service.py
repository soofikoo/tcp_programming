from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import User


def create_user(session: Session, username: str, email: str, password_hash: str, role: str) -> User:
    """password_hash — уже захэшированный пароль (хэширует api/security.py)."""
    user = User(username=username, email=email, password_hash=password_hash, role=role)
    session.add(user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("User already exists")
    session.refresh(user)
    return user


def update_user(session: Session, user_id: int,
                username: str | None = None,
                email: str | None = None) -> User | None:
    user = session.get(User, user_id)
    if user is None:
        return None
    if username is not None:
        user.username = username
    if email is not None:
        user.email = email
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("Username or email already taken")
    session.refresh(user)
    return user


def delete_user(session: Session, user_id: int) -> bool:
    result = session.execute(delete(User).where(User.id == user_id))
    session.commit()
    return result.rowcount > 0


def get_user(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)


def get_user_by_username(session: Session, username: str) -> User | None:
    return session.execute(select(User).where(User.username == username)).scalar_one_or_none()
