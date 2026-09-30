from datetime import datetime
from sqlalchemy import DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base_model import Base


class Subscriptions(Base):
    __tablename__ = "subscriptions"

    subscription_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete = 'CASCADE'), primary_key=True)
    artist_id: Mapped[int] = mapped_column(ForeignKey("artists.id", ondelete = 'CASCADE'), primary_key=True)
    subscribed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())