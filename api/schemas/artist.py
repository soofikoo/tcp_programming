from pydantic import BaseModel, ConfigDict


class ArtistOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    artist_id: int
    bio: str

class ArtistUpdate(BaseModel):
    bio: str