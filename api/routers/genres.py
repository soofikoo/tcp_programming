from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session as DbSession

from api.deps import get_db, require_role
from api.schemas.genre import GenreOut, GenreCreate, GenreUpdate
from models import User
from services.genres_service import get_genre, create_genre, update_genre, delete_genre

router = APIRouter(prefix="/genres", tags=["genres"])

@router.get("/{genre_id}", response_model=GenreOut)
def get_genre_by_id(genre_id: int, db: DbSession = Depends(get_db)):
    genre = get_genre(db, genre_id)
    if genre is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Genre not found")
    return genre


@router.post("", response_model=GenreOut, status_code=status.HTTP_201_CREATED)
def create(body: GenreCreate, db: DbSession = Depends(get_db),
                       user: User = Depends(require_role("artist"))):
    try:
        return create_genre(db, body.name)
    except ValueError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e))


@router.patch("/{genre_id}", response_model=GenreOut)
def patch_genre(genre_id: int, body: GenreUpdate, db: DbSession = Depends(get_db),
                user: User = Depends(require_role("artist"))):
    if get_genre(db, genre_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Genre not found")
    try:
        return update_genre(db, genre_id, body.name)
    except ValueError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e))


@router.delete("/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(genre_id: int, db: DbSession = Depends(get_db),
                       user: User = Depends(require_role("artist"))):
    if not delete_genre(db, genre_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Genre not found")
