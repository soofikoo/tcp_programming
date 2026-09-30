from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base_model import Base
from models.genre_model import Genre

if TYPE_CHECKING:
    from models.album_model import Album

class Track(Base):
    __tablename__ = 'track'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    album_id: Mapped[int | None] = mapped_column(ForeignKey('album.id'))
    duration: Mapped[int] = mapped_column()
    file_path: Mapped[str] = mapped_column(String(256))
    upload_date: Mapped[datetime] = mapped_column(DateTime)
    artist_id: Mapped[int] = mapped_column(ForeignKey('artist.artist_id', ondelete = 'CASCADE'))
    # TODO
    genres: Mapped[list["Genre"]] = relationship(secondary="track_genre")
    album: Mapped["Album | None"] = relationship(back_populates="tracks")

