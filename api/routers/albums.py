from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session as DbSession

from api.deps import get_db, require_role
from api.schemas.album import AlbumOut, AlbumCreate, AlbumUpdate, AlbumPage
from models import User
from services.albums_service import get_album, create_album, update_album, delete_album

router = APIRouter(prefix="/albums", tags=["albums"])


@router.get("/{album_id}", response_model=AlbumPage)
def get_album_page(album_id: int, db: DbSession = Depends(get_db)):
    album = get_album(db, album_id)
    if album is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Album not found")
    return album   # album.tracks подгрузится лениво, пока сессия открыта


@router.post("", response_model=AlbumOut, status_code=status.HTTP_201_CREATED)
def create_album_for_user(body: AlbumCreate, db: DbSession = Depends(get_db),
                          user: User = Depends(require_role("artist"))):
    return create_album(db, body.title, user.id, body.release_date, body.cover_url)


@router.patch("/{album_id}", response_model=AlbumOut)
def patch_album(album_id: int, body: AlbumUpdate, db: DbSession = Depends(get_db),
                user: User = Depends(require_role("artist"))):
    album = get_album(db, album_id)
    if album is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Album not found")
    if album.artist_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not your album")
    data = body.model_dump(exclude_unset=True)   # только присланные поля
    return update_album(
        db, album.id,
        data.get("title", album.title),
        data.get("release_date", album.release_date),
        data.get("cover_url", album.cover_url),
    )


@router.delete("/{album_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_own_album(album_id: int, db: DbSession = Depends(get_db),
                     user: User = Depends(require_role("artist"))):
    album = get_album(db, album_id)
    if album is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Album not found")
    if album.artist_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not your album")
    delete_album(db, album_id)
