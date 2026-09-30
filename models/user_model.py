from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base_model import Base

if TYPE_CHECKING:
    from models.artist_profile_model import Artist


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)  # SERIAL создаётся автоматически для Integer + primary_key
    username: Mapped[str] = mapped_column(String(64), unique=True)
    email: Mapped[str] = mapped_column(String(128), unique=True)
    password_hash: Mapped[str] = mapped_column(String(256))
    role: Mapped[str] = mapped_column(String(16))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    __table_args__ = (
        CheckConstraint("role IN ('listener', 'artist')", name="ck_users_role"),
    )

    artist: Mapped["Artist"] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"Users(id={self.id!r}, username={self.username!r})"