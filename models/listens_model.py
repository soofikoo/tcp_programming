from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, CheckConstraint, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from models.user_model import User
from models.tracks_model import Track
from models.base_model import Base


class Listens(Base):
    __tablename__ = "listens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete = 'CASCADE'))
    track_id: Mapped[int] = mapped_column(ForeignKey("tracks.id", ondelete = 'CASCADE'))
    listened_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    user: Mapped["User"] = relationship(uselist=False)
    track: Mapped["Track"] = relationship(uselist=False)