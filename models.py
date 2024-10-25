from sqlalchemy import (
    Table,
    Integer,
    String,
    Text,
    Column,
    DateTime,
    ForeignKey,
    Boolean,
)
from datetime import datetime

from .database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    hashed_password = Column(Text, nullable=False)
    disabled = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
