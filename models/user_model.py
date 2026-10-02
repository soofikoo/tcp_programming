from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base_model import Base
from models.time_model import TimeStamptedModel

if TYPE_CHECKING:
    from models.artist_profile_model import Artist


class User(TimeStamptedModel):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)  # SERIAL создаётся автоматически для Integer + primary_key
    username: Mapped[str] = mapped_column(String(64), unique=True)
    email: Mapped[str] = mapped_column(String(128), unique=True)
    password_hash: Mapped[str] = mapped_column(String(256))
    role: Mapped[str] = mapped_column(String(16))


    __table_args__ = (
        CheckConstraint("role IN ('listener', 'artist')", name="ck_users_role"),
    )

    artist: Mapped["Artist"] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"Users(id={self.id!r}, username={self.username!r})"