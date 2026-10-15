import jwt
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from api.security import decode_token
from sqlalchemy.orm import Session as DbSession

from database import Session
from models import User
from services.user_service import get_users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    with Session() as session:
        yield session


def get_current_user(token: str = Depends(oauth2_scheme), db: DbSession = Depends(get_db)):
    try:
        user_id = int(decode_token(token)["sub"])
    except jwt.PyJWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")
    user = get_users(db, user_id)
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not found")
    return user

def require_role(role: str):
    def checker(user: User = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Not enough rights")
        return user
    return checker

