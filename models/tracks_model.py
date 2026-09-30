from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from models.likes_model import Likes
from models.genres_model import Genres
from models.base_model import Base


# todo (s) создать связи к имени артиста, нужен ли дефолт в дате?
# убрал play_count - кринжа полная
class Track(Base):
    __tablename__ = 'tracks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    album_id: Mapped[int] = mapped_column(ForeignKey('Albums.id'), ondelete = 'SET NULL')
    duration: Mapped[int] = mapped_column()
    file_path: Mapped[str] = mapped_column(String(256))
    upload_date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    artist_id: Mapped[int] = mapped_column(ForeignKey('Artists.id'), ondelete = 'CASCADE')

    genres: Mapped[list["Genres"]] = relationship(secondary="track_genres")

