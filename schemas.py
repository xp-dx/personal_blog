from pydantic import BaseModel


class AllArticles(BaseModel):
    id: int
    title: str
    created_at: str


class Article(AllArticles):
    content: str


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    disabled: bool = False


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
