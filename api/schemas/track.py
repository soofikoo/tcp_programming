from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TrackCreate(BaseModel):
    title: str = Field(min_length=1, max_length=128)
    album_id: int | None = None
    duration: int = Field(gt=0, description="Длительность в секундах")
    file_path: str = Field(max_length=256)


class TrackUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=128)
    album_id: int | None = None


class TrackOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    album_id: int | None
    duration: int
    file_path: str
    upload_date: datetime
    artist_id: int


class TrackListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    duration: int
    file_path: str
    artist_name: str


class LikedTrack(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    duration: int
    artist_name: str
    liked_at: datetime
