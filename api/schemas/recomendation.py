from pydantic import BaseModel


class RecommendationOut(BaseModel):
    track_id: int
    title: str
    artist_name: str
    score: float
    reason: str