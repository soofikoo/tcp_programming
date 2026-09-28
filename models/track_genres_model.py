from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, CheckConstraint, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from models.base_model import Base

#
class TrackGenre(Base):
    __tablename__ = "track_genres"

    track_id: Mapped[int] = mapped_column(ForeignKey("Tracks.id", ondelete="CASCADE"), primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("Genres.id", ondelete="CASCADE"), primary_key=True)

