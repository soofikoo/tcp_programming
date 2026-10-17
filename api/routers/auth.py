from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session as DbSession

from api.deps import get_db
from api.schemas.user import UserOut, UserRegister, Token
from api.security import hash_password, verify_password, create_access_tokes
from services.artist_profiles_service import create_artist
from services.user_service import create_user, get_user_by_username

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(body: UserRegister, db: DbSession = Depends(get_db)):
    try:
        user = create_user(db, body.username, body.email, hash_password(body.password), body.role)
    except ValueError:
        raise HTTPException(status.HTTP_409_CONFLICT, "Username or email already taken")
    if body.role == "artist":
        create_artist(db, user.id)
    return user


@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: DbSession = Depends(get_db)):
    user = get_user_by_username(db, form.username)
    if user is None or not verify_password(form.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect username or password")
    return Token(access_token=create_access_tokes(user.id, user.role))
