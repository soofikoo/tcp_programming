from pydantic import BaseModel


class Like(BaseModel):
    track_id: int
    user_id: int