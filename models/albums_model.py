from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from models.base_model import Base


# TODO наверно надо добавить связи к трекам (двустороннею) и артисту (тут хз какая связь)(одностроняя наверн)
class Album(Base):
    __tablename__ = "Album"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    artist_id: Mapped[int] = mapped_column(ForeignKey("Users.id", ondelete="CASCADE"))
    release_date: Mapped[datetime] = mapped_column(DateTime)
    cover_url: Mapped[str] = mapped_column(String(256))