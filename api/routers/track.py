from fastapi import APIRouter, Depends, HTTPException, status, Query

from api.deps import get_db, require_role
from api.schemas.track import TrackCreate, TrackUpdate, TrackOut
from models import User
from services.genres_service import get_genre
from services.track_genres_service import create_track_genre, delete_track_genre
from services.tracks_service import create_track, get_track, get_track_list_by_genre, update_track, delete_track
from sqlalchemy.orm import Session as DbSession

router = APIRouter(prefix="/tracks", tags=["tracks"])

@router.get("/{track_id}", response_model=TrackOut)
def get_track_by_id(track_id: int, db: DbSession = Depends(get_db)):
    track = get_track(db, track_id)
    if not track:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Track not found")
    return track

@router.get("", response_model=list[TrackOut])
def get_track_by_genre(genre_ids: list[int] | None = Query(None), db: DbSession = Depends(get_db)):
    if genre_ids:
        return get_track_list_by_genre(db, genre_ids)
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Genre not found")

@router.post("", response_model=TrackOut)
def add_track(body: TrackCreate, db: DbSession = Depends(get_db), user: User = Depends(require_role("artist"))):
    return create_track(db, body.title, body.album_id, body.duration, body.file_path, body.upload_date, user.id)

@router.patch("/{track_id}", response_model=TrackOut)
def patch_track(track_id: int, body: TrackUpdate, db: DbSession = Depends(get_db), user: User = Depends(require_role("artist"))):
    track = get_track(db, track_id)
    if not track:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Track not found")
    if track.artist_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not your track")
    data = body.model_dump(exclude_unset=True)
    update_track(
        db,
        track.id,
        data.get("title", track.title),
    )
    return get_track(db, track.id)

@router.delete("/{track_id}", status_code=status.HTTP_204_NO_CONTENT)
def drop_track(track_id: int, db: DbSession = Depends(get_db), user: User = Depends(require_role("artist"))):
    track = get_track(db, track_id)
    if not track:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Track not found")
    if track.artist_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not your track")
    delete_track(db, track.id)

@router.post("/{track_id}/genres/{genre_id}", status_code=status.HTTP_201_CREATED)
def add_genre_track(track_id: int, genre_id: int, db: DbSession = Depends(get_db), user: User = Depends(require_role("artist"))):
    track = get_track(db, track_id)
    if not track:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Track not found")
    if track.artist_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not your track")
    genre = get_genre(db, genre_id)
    if not genre:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Genre not found")
    create_track_genre(db, track_id, genre_id)

@router.delete("/{track_id}/genres/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
def add_genre_track(track_id: int, genre_id: int, db: DbSession = Depends(get_db), user: User = Depends(require_role("artist"))):
    track = get_track(db, track_id)
    if not track:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Track not found")
    if track.artist_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not your track")
    genre = get_genre(db, genre_id)
    if not genre:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Genre not found")
    delete_track_genre(db, track_id, genre_id)