from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base_model import Base


class TrackGenre(Base):
    __tablename__ = "track_genre"

    track_id: Mapped[int] = mapped_column(ForeignKey("track.id", ondelete="CASCADE"), primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genre.id", ondelete="CASCADE"), primary_key=True)