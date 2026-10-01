from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import User


def create_user(session: Session, username: str, email: str, password: str, role: str) -> User:
    user = User(
        username=username,
        email=email,
        password_hash=password,
        role=role,
    )
    session.add(user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("User already exists")
    return user

#def update_user(session: Session, ) -> Users:
#    что-то я хз как тут сделать
# todo (s) понять какой апдейт делать
def delete_user(session: Session, user_id: int) -> bool:
    result = session.execute(delete(User).where(User.id == user_id))
    session.commit()
    return result.rowcount > 0

def get_users(session: Session, user_id: int) -> User | None:
    return session.execute(select(User).where(User.id == user_id)).scalar_one_or_none()