from datetime import datetime, date

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Track
from models.user_model import User
from models.base_model import Base


class Album(Base):
    __tablename__ = "album"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    artist_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    release_date: Mapped[date] = mapped_column()
    cover_url: Mapped[str] = mapped_column(String(256))

    artist: Mapped["User"] = relationship()
    tracks: Mapped[list["Track"]] = relationship(back_populates="album")