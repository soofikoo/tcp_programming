from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Album(Base):
    __tablename__ = "Album"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    artist_id: Mapped[int] = mapped_column(ForeignKey("User.id", ondelete="CASCADE"))
    release_date: Mapped[datetime] = mapped_column(DateTime)
    cover_url: Mapped[str] = mapped_column(String(256))