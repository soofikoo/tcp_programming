from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, CheckConstraint, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)  # SERIAL создаётся автоматически для Integer + primary_key
    username = Column(String(64), nullable=False, unique=True)
    email = Column(String(128), nullable=False, unique=True)
    password_hash = Column(String(256), nullable=False)
    role = Column(String(16), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    __table_args__ = (
        CheckConstraint("role IN ('listener', 'artist')", name="ck_users_role"),
    )


engine = create_engine("postgresql://postgres:pass@localhost:5432/music")
Base.metadata.create_all(engine)