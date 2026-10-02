from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base_model import Base

if TYPE_CHECKING:
    from models.user_model import User


class Artist(Base):
    __tablename__ = 'artist'

    artist_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    bio: Mapped[str | None] = mapped_column(String(256))

    user: Mapped["User"] = relationship(back_populates="artist")
