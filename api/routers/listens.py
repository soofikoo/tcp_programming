from fastapi import APIRouter, Depends, HTTPException, status, Query

from api.deps import get_db, require_role, get_current_user
from api.schemas.track import TrackCreate, TrackUpdate, TrackOut
from models import User
from services.genres_service import get_genre
from services.listens_service import create_listen
from services.track_genres_service import create_track_genre, delete_track_genre
from services.tracks_service import create_track, get_track, get_track_list_by_genre, update_track, delete_track
from sqlalchemy.orm import Session as DbSession

router = APIRouter(prefix="/listens", tags=["listens"])

@router.post("/{track_id}", status_code=status.HTTP_201_CREATED)
def create_listen_track(track_id: int, user: User = Depends(get_current_user), db: DbSession = Depends(get_db)):
    track = get_track(db, track_id)
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")
    create_listen(db, user.id, track_id)
