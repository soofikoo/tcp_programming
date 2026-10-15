from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session as DbSession

from api import deps
from api.deps import get_db
from api.schemas.artist import ArtistUpdate, ArtistOut
from models import User
from services.artist_profiles_service import get_artist, update_artist

router = APIRouter(prefix="/artist", tags=["artist"])

@router.patch("/{artist_id}", response_model=ArtistOut)
def patch_artist_profile(artist_id: int, body: ArtistUpdate,
                         db: DbSession = Depends(get_db),
                         user: User = Depends(deps.require_role("artist"))):
    if artist_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not your profile")
    artist = get_artist(db, artist_id)
    if artist is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Artist not found")
    data = body.model_dump(exclude_unset=True)
    update_artist(db, artist_id, data.get("bio", artist.bio))
    return get_artist(db, artist_id)