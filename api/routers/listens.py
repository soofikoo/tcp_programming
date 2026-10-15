from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session as DbSession

from api.deps import get_db, get_current_user
from models import User
from services.listens_service import create_listen
from services.tracks_service import get_track

router = APIRouter(prefix="/listens", tags=["listens"])

@router.post("/{track_id}", status_code=status.HTTP_201_CREATED)
def create_listen_track(track_id: int, user: User = Depends(get_current_user), db: DbSession = Depends(get_db)):
    track = get_track(db, track_id)
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")
    create_listen(db, user.id, track_id)
