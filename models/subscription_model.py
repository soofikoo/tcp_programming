from datetime import datetime
from sqlalchemy import DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base_model import Base


class Subscription(Base):
    __tablename__ = "subscription"

    subscription_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete = 'CASCADE'), primary_key=True)
    artist_id: Mapped[int] = mapped_column(ForeignKey("artist.artist_id", ondelete = 'CASCADE'), primary_key=True)
    subscribed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())