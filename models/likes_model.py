from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base_model import Base
from models.tracks_model import Track
from models.user_model import User


# TODO по идеи убрать двухстороннею или вообще убрать как в listens
class Likes(Base):
    __tablename__ = 'likes'

    user_id: Mapped[int] = mapped_column(ForeignKey("User.id", ondelete="CASCADE"), primary_key=True)
    track_id: Mapped[int] = mapped_column(ForeignKey("Track.id", ondelete="CASCADE"), primary_key=True)
    listened_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="likes")
    track: Mapped["Track"] = relationship(back_populates="likes")