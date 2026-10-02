from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.time_model import TimeStamptedModel


class Listen(TimeStamptedModel):
    __tablename__ = "listen"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete = 'CASCADE'))
    track_id: Mapped[int] = mapped_column(ForeignKey("track.id", ondelete = 'CASCADE'))
