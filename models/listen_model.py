from datetime import datetime

from sqlalchemy import DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base_model import Base


class Listen(Base):
    __tablename__ = "listen"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete = 'CASCADE'))
    track_id: Mapped[int] = mapped_column(ForeignKey("track.id", ondelete = 'CASCADE'))
    listened_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())