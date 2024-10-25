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


# fake_users_db = {
#     "akito": {
#         "username": "akito",
#         "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#         "disabled": False,
#     }
# }

# fake_articles_db = [
#     {
#         "id": 0,
#         "title": "Article 1",
#         "content": "Content of article 1",
#         "created_at": "October 20, 2024",
#     },
#     {
#         "id": 1,
#         "title": "Article 2",
#         "content": "Content of article 2",
#         "created_at": "October 21, 2024",
#     },
# ]
