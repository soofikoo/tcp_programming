from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session as DbSession

from api.deps import get_db, get_current_user
from api.schemas.like import Like
from models import User

router = APIRouter(prefix="/likes", tags=["likes"])

@router.get("/", response_model=list[Like])
def get_likes_by_user(db: DbSession = Depends(get_db), user: User = Depends(get_current_user)):
    return get_likes_by_user(db, user)