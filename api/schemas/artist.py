from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from api.schemas.album import AlbumOut


class ArtistOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    artist_id: int
    bio: str | None


class ArtistUpdate(BaseModel):
    bio: str | None = Field(default=None, max_length=256)


class ArtistPage(BaseModel):
    artist_id: int
    name: str
    bio: str | None
    subscribers: int

class SubscriptionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    artist_id: int
    artist_name: str
    subscribed_at: datetime
