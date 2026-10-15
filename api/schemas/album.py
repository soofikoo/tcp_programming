from datetime import date

from pydantic import BaseModel, ConfigDict


class AlbumCreate(BaseModel):
    title: str
    release_date: date
    cover_url: str

class AlbumUpdate(BaseModel):
    title: str | None = None
    release_date: date | None = None
    cover_url: str | None = None

class AlbumOut(BaseModel):
    id: int
    title: str
    artist_id: int
    release_date: date
    cover_url: str

class TrackShort(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    duration: int

class AlbumPage(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    tracks: list[TrackShort]
