from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, CheckConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

# TODO кирилл

class Genres(Base):
    __tablename__ = "genres"








    tracks: Mapped[list["Track"]] = relationship(secondary="track_genres", back_populates="genres")