from sqlalchemy import update, select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from models import Users


def create_user(session: Session, username: str, email: str, password: str, role: str) -> Users:
    user = Users(
        username=username,
        email=email,
        password=password,
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
    result = session.execute(delete(Users).where(Users.id == user_id))
    return result.rowcount > 0

def get_users(session: Session, user_id: int) -> Users | None:
    return session.execute(select(Users).where(Users.id == user_id)).scalar_one_or_none()