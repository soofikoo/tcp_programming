from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from models.base_model import Base


class Like(Base):
    __tablename__ = 'like'

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    track_id: Mapped[int] = mapped_column(ForeignKey("track.id", ondelete="CASCADE"), primary_key=True)
    likes_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())