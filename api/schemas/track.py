from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TrackCreate(BaseModel):
    title: str
    album_id: int
    duration: int
    file_path: str
    upload_date: datetime

class TrackUpdate(BaseModel):
    title: str | None = None

class TrackOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    album_id: int
    duration: int
    file_path: str
    upload_date: datetime
    artist_id: int