from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models.base_model import Base


class Genre(Base):
    __tablename__ = "genre"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)