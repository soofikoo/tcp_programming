from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from models.base_model import Base


class Likes(Base):
    __tablename__ = 'likes'

    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id", ondelete="CASCADE"), primary_key=True)
    track_id: Mapped[int] = mapped_column(ForeignKey("Track.id", ondelete="CASCADE"), primary_key=True)
    listened_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())