from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, CheckConstraint, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Track(Base):
    __tablename__ = 'tracks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    album_id: Mapped[int] = mapped_column(ForeignKey('Albums.id'), ondelete = 'SET NULL')
    duration: Mapped[int] = mapped_column()
    file_path: Mapped[str] = mapped_column(String(256))
    upload_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    play_count: Mapped[int] = mapped_column(default=0)