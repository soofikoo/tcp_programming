from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from models.base_model import Base

# TODO двусторонняя надо для user наверн
class Artist(Base):
    __tablename__ = 'artist'

    artist_id: Mapped[int] = mapped_column(ForeignKey("User.id", ondelete="CASCADE"), primary_key=True)
    bio: Mapped[str | None] = mapped_column(String(256))
