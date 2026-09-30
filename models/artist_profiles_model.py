from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from models.base_model import Base
from models.user_model import Users


class Artist(Base):
    __tablename__ = 'artist'

    artist_id: Mapped[int] = mapped_column(ForeignKey("Users.id", ondelete="CASCADE"), primary_key=True)
    bio: Mapped[str | None] = mapped_column(String(256))

    users: Mapped[Users] = relationship(back_populates="artist")
