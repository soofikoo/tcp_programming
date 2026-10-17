from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session as DbSession

from api.deps import get_db, get_current_user, require_role
from api.schemas.artist import ArtistOut, ArtistUpdate, ArtistPage
from models import User
from services.artist_profiles_service import get_artist, update_artist
from services.subscriptions_service import (create_subscription, delete_subscription,
                                            count_subscription_by_artist)

router = APIRouter(prefix="/artists", tags=["artists"])


@router.get("/{artist_id}", response_model=ArtistPage)
def get_artist_page(artist_id: int, db: DbSession = Depends(get_db)):
    artist = get_artist(db, artist_id)
    if artist is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Artist not found")
    return ArtistPage(
        artist_id=artist.artist_id,
        name=artist.user.username,
        bio=artist.bio,
        subscribers=count_subscription_by_artist(db, artist_id)
    )


@router.patch("/{artist_id}", response_model=ArtistOut)
def patch_artist_profile(artist_id: int, body: ArtistUpdate, db: DbSession = Depends(get_db),
                         user: User = Depends(require_role("artist"))):
    if artist_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not your profile")
    artist = get_artist(db, artist_id)
    if artist is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Artist not found")
    data = body.model_dump(exclude_unset=True)
    return update_artist(db, artist_id, data.get("bio", artist.bio))


@router.post("/{artist_id}/subscribe", status_code=status.HTTP_201_CREATED)
def add_subscribe(artist_id: int, db: DbSession = Depends(get_db),
                  user: User = Depends(get_current_user)):
    if get_artist(db, artist_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Artist not found")
    if artist_id == user.id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Cannot subscribe to yourself")
    try:
        create_subscription(db, user.id, artist_id)
    except ValueError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e))
    return {"artist_id": artist_id, "subscribed": True}


@router.delete("/{artist_id}/subscribe", status_code=status.HTTP_204_NO_CONTENT)
def remove_subscribe(artist_id: int, db: DbSession = Depends(get_db),
                     user: User = Depends(get_current_user)):
    if not delete_subscription(db, user.id, artist_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Subscription not found")
