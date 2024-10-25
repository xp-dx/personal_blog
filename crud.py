from sqlalchemy.orm import Session

from . import models, schemas, config
from .password_hashing import get_password_hash, verify_password
import json
from datetime import timedelta, datetime, timezone
import jwt
from typing import Annotated


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=5)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


def get_article_by_title(db: Session, title: str):
    return db.query(models.Article).filter(models.Article.title == title).first()


def get_article_by_id(db: Session, id: int):
    return db.query(models.Article).filter(models.Article.id == id).first()


def get_all_articles(db: Session):
    articles = db.query(models.Article.title, models.Article.created_at).all()
    articles_json = []
    for article in articles:
        articles_json.append({"title": article[0], "created_at": article[1]})
    return json.loads(json.dumps(articles_json, default=str))


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_article(db: Session, article: schemas.ArticleCreate):
    db_artcile = models.Article(title=article.title, content=article.content)
    db.add(db_artcile)
    db.commit()
    db.refresh(db_artcile)
    return db_artcile


def delete_user(db: Session, db_user: schemas.User):
    db.delete(db_user)
    db.commit()
    return {"message": "Successfully deleted user"}


def delete_article(db: Session, db_article: schemas.Article):
    db.delete(db_article)
    db.commit()
    return {"message": "Successfully deleted article"}


def update_article(
    db: Session, article: schemas.Article, new_article: schemas.ArticleCreate
):
    article.title = new_article.title
    article.content = new_article.content
    db.add(article)
    db.commit()
    db.refresh(article)
    return article
