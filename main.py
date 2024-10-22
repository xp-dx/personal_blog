from fastapi import FastAPI, HTTPException, status, Depends
from . import models, schemas, crud
from datetime import datetime
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .password_hashing import get_password_hash

app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
models.Base.metadata.create_all(engine)


def get_all_articles():
    return models.fake_articles_db


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/home")
async def home():
    return models.fake_articles_db


@app.get("/article/{article_id}")
async def article(article_id: int):
    if article_id not in models.fake_articles_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="article doesn't exist"
        )
    return models.fake_articles_db[article_id]


@app.get("/admin")
async def admin():
    return {"message": "Hello Admin"}


@app.post("/user/create/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username already exists"
        )
    return crud.create_user(db=db, user=user)


@app.delete("/user/delete/")
def delete_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist"
        )
    return crud.delete_user(db=db, db_user=db_user)


@app.patch("/edit/{article_id}")
async def edit(article_id: int):
    return {"article_id": article_id}


@app.post("/new")
async def new():
    return {"message": "Hello New"}
