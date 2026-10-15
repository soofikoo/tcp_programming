from fastapi import APIRouter, status, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session as DbSession

from api.deps import get_db, get_current_user
from api.schemas.like import Like
from models import User
from services.likes_service import create_like, delete_like
from services.tracks_service import get_track

router = APIRouter(prefix="/likes", tags=["likes"])

@router.get("/", response_model=list[Like])
def get_likes_by_user(db: DbSession = Depends(get_db), user: User = Depends(get_current_user)):
    return get_likes_by_user(db, user)

@router.post("/{track_id}", status_code=status.HTTP_201_CREATED)
def add_like(track_id: int, user: User = Depends(get_current_user), db: DbSession = Depends(get_db)):
    track = get_track(db, track_id)
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")
    try:
        create_like(db, user.id, track_id)
    except ValueError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e))

@router.delete("/{track_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_like(track_id: int, user: User = Depends(get_current_user), db: DbSession = Depends(get_db)):
    track = get_track(db, track_id)
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")
    try:
        delete_like(db, user.id, track_id)
    except ValueError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))