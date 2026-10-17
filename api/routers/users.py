from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session as DbSession

from api.deps import get_db, get_current_user
from api.schemas.artist import SubscriptionOut
from api.schemas.track import LikedTrack
from api.schemas.user import UserOut, UserUpdate
from models import User
from services.likes_service import get_liked_track
from services.subscriptions_service import get_subscription_by_user
from services.user_service import update_user

router = APIRouter(prefix="/me", tags=["me"])


@router.get("", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user


@router.patch("", response_model=UserOut)
def patch_me(body: UserUpdate, db: DbSession = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        return update_user(db, user.id, **body.model_dump(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e))


@router.get("/likes", response_model=list[LikedTrack])
def my_likes(db: DbSession = Depends(get_db), user: User = Depends(get_current_user)):
    return get_liked_track(db, user.id)


@router.get("/subscriptions", response_model=list[SubscriptionOut])
def my_subscriptions(db: DbSession = Depends(get_db), user: User = Depends(get_current_user)):
    return get_subscription_by_user(db, user.id)
