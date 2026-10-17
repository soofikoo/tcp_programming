from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class AlbumCreate(BaseModel):
    title: str = Field(min_length=1, max_length=128)
    release_date: date
    cover_url: str | None = Field(default=None, max_length=256)


class AlbumUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=128)
    release_date: date | None = None
    cover_url: str | None = Field(default=None, max_length=256)


class AlbumOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    artist_id: int
    release_date: date
    cover_url: str | None


class TrackShort(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    duration: int


class AlbumPage(AlbumOut):
    tracks: list[TrackShort]
