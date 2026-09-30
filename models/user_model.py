from datetime import datetime
from sqlalchemy import create_engine, String, CheckConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from models.artist_profiles_model import Artist
from models.base_model import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)  # SERIAL создаётся автоматически для Integer + primary_key
    username: Mapped[str] = mapped_column(String(64), unique=True)
    email: Mapped[str] = mapped_column(String(128), unique=True)
    password_hash: Mapped[str] = mapped_column(String(256))
    role: Mapped[str] = mapped_column(String(16))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    __table_args__ = (
        CheckConstraint("role IN ('listener', 'artist')", name="ck_users_role"),
    )

    # TODO надо back_populates для связи
    #likes: Mapped[list["Likes"]] = relationship(back_populates="user", cascade="all, delete-orphan", passive_deletes=True)


    def __repr__(self) -> str:
        return f"Users(id={self.id!r}, username={self.username!r})"

    artist: Mapped[Artist] = relationship(back_populates="users")
# engine = create_engine("postgresql://postgres:pass@localhost:5432/music", echo = True)
# Base.metadata.create_all(engine)
# todo (s) создать связи, лайки, подписки