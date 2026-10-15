from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session as DbSession

from api import deps
from api.schemas.user import UserOut
from api.security import verify_password, create_access_tokes
from models import User
from services.user_service import get_user_by_username

router = APIRouter(prefix="/login", tags=["auth"])

@router.post("")
def login(form: OAuth2PasswordRequestForm = Depends(), db:DbSession = Depends(deps.get_db)):
    user = get_user_by_username(db, form.username)
    if user is None or not verify_password(form.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return {"access_token": create_access_tokes(user.id, user.role), "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def me(user: User = Depends(deps.get_current_user)):
    return user