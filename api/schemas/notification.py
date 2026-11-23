from datetime import datetime
from pydantic import BaseModel

from messaging import TRACK_CREATED


class TrackCreatedEvent(BaseModel):
    event: str = TRACK_CREATED
    track_id: int
    title: str
    artist_id: int
    artist_name: str
    subscriber_ids: list[int]
    created_at: datetime
