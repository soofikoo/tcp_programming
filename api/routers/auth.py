from fastapi import APIRouter, Depends, HTTPException, status

from api.deps import get_db
from api.schemas.user import UserOut, UserRegister
from api.security import hash_password
from services.user_service import create_user
from services.artist_profiles_service import create_artist
from sqlalchemy.orm import Session as DbSession
router = APIRouter(prefix="/register", tags=["auth"])

@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(body: UserRegister, db: DbSession = Depends(get_db)):
    try:
        body.password = hash_password(body.password)
        user = create_user(db, body.username, body.email, body.password, body.role)
        if body.role == "artist":
            create_artist(db, user.id, "")
        return user
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))