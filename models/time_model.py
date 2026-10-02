from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column
from datetime import datetime

from models import Base


class TimeStamptedModel(Base):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), server_onupdate=func.now())