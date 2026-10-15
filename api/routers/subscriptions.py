from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session as DbSession

from api.deps import get_db, get_current_user
from models import User
from services.artist_profiles_service import get_artist
from services.subscriptions_service import create_subscription, delete_subscription

router = APIRouter(prefix="/subscribe", tags=["subscribe"])

@router.post("/{artist_id}", status_code=status.HTTP_201_CREATED)
def add_subscribe(
        artist_id: int,
        db: DbSession = Depends(get_db),
        user: User = Depends(get_current_user)
    ):
    if get_artist(db, artist_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Artist not found")
    if artist_id == user.id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Cannot subscribe to yourself")
    try:
        create_subscription(db, user.id, artist_id)
    except ValueError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e))

@router.delete("/{artist_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_subscribe(
        artist_id: int,
        db: DbSession = Depends(get_db),
        user: User = Depends(get_current_user)
    ):
    if not delete_subscription(db, user.id, artist_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Subscription not found")