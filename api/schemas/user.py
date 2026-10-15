from typing import Literal

from pydantic import BaseModel, Field, ConfigDict


class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    email: str
    password: str = Field(min_length=6)
    role: Literal["listener", "artist"] = "listener"

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: str
    role: str
