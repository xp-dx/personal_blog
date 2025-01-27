from pydantic import BaseModel, ValidationError
from datetime import datetime


class ArticleBase(BaseModel):
    title: str


class ArticleCreate(ArticleBase):
    content: str


class ArticleUpdate(ArticleCreate):
    created_at: datetime


class Article(ArticleCreate):
    id: int
    created_at: datetime


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    disabled: bool = False


class Admin(User):
    is_superuser: bool = False


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    # scopes: list[str] = []


class FormData(BaseModel):
    username: str
    password: str
