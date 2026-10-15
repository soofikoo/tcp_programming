from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session as DbSession

from api.deps import get_db, require_role, get_current_user
from api.schemas.track import TrackCreate, TrackUpdate, TrackOut, TrackListItem
from models import User
from services.albums_service import get_album
from services.genres_service import get_genre
from services.likes_service import create_like, delete_like
from services.listens_service import create_listen
from services.track_genres_service import create_track_genre, delete_track_genre
from services.tracks_service import (create_track, get_track, get_track_list_by_genre,
                                     get_track_player, update_track, delete_track)

router = APIRouter(prefix="/tracks", tags=["tracks"])


# ---------- CRUD ----------

@router.get("/{track_id}", response_model=TrackListItem)
def get_track_by_id(track_id: int, db: DbSession = Depends(get_db)):
    track = get_track_player(db, track_id)
    if track is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Track not found")
    return track


@router.post("", response_model=TrackOut, status_code=status.HTTP_201_CREATED)
def add_track(body: TrackCreate, db: DbSession = Depends(get_db),
              user: User = Depends(require_role("artist"))):
    if body.album_id is not None:
        album = get_album(db, body.album_id)
        if album is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Album not found")
        if album.artist_id != user.id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Not your album")
    return create_track(db, body.title, body.album_id, body.duration, body.file_path, user.id)


@router.patch("/{track_id}", response_model=TrackOut)
def patch_track(track_id: int, body: TrackUpdate, db: DbSession = Depends(get_db),
                user: User = Depends(require_role("artist"))):
    track = get_track(db, track_id)
    if track is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Track not found")
    if track.artist_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not your track")
    data = body.model_dump(exclude_unset=True)   # только присланные поля
    if data.get("album_id") is not None:
        album = get_album(db, data["album_id"])
        if album is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Album not found")
        if album.artist_id != user.id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Not your album")
    return update_track(db, track.id, data.get("title", track.title), data.get("album_id", track.album_id))


@router.delete("/{track_id}", status_code=status.HTTP_204_NO_CONTENT)
def drop_track(track_id: int, db: DbSession = Depends(get_db),
               user: User = Depends(require_role("artist"))):
    track = get_track(db, track_id)
    if track is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Track not found")
    if track.artist_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not your track")
    delete_track(db, track_id)


# Жанры треков

@router.post("/{track_id}/genres/{genre_id}", status_code=status.HTTP_201_CREATED)
def add_genre_track(track_id: int, genre_id: int, db: DbSession = Depends(get_db),
                    user: User = Depends(require_role("artist"))):
    track = get_track(db, track_id)
    if track is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Track not found")
    if track.artist_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not your track")
    if get_genre(db, genre_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Genre not found")
    try:
        create_track_genre(db, track_id, genre_id)
    except ValueError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e))
    return {"track_id": track_id, "genre_id": genre_id}


@router.delete("/{track_id}/genres/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_genre_track(track_id: int, genre_id: int, db: DbSession = Depends(get_db),
                       user: User = Depends(require_role("artist"))):
    track = get_track(db, track_id)
    if track is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Track not found")
    if track.artist_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not your track")
    if not delete_track_genre(db, track_id, genre_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Track has no such genre")


# Лайки нелайки

@router.post("/{track_id}/listen", status_code=status.HTTP_201_CREATED)
def create_listen_track(track_id: int, db: DbSession = Depends(get_db),
                        user: User = Depends(get_current_user)):
    if get_track(db, track_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Track not found")
    listen = create_listen(db, user.id, track_id)
    return {"track_id": track_id, "listened_at": listen.created_at}


@router.post("/{track_id}/like", status_code=status.HTTP_201_CREATED)
def add_like(track_id: int, db: DbSession = Depends(get_db),
             user: User = Depends(get_current_user)):
    if get_track(db, track_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Track not found")
    try:
        create_like(db, user.id, track_id)
    except ValueError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e))
    return {"track_id": track_id, "liked": True}


@router.delete("/{track_id}/like", status_code=status.HTTP_204_NO_CONTENT)
def remove_like(track_id: int, db: DbSession = Depends(get_db),
                user: User = Depends(get_current_user)):
    if not delete_like(db, user.id, track_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Like not found")
