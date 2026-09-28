from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, CheckConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from models.base_model import Base


class Genres(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)