from fastapi import FastAPI, HTTPException, status, Depends
from . import models, schemas, crud
from datetime import datetime, timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> schemas.Token:
    user = crud.authenticate_user(
        models.fake_users_db, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
    )
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


@app.get("/admin")
async def admin():
    return {"message": "Hello Admin"}


@app.post("/user/create/", tags=["users"], response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username already exists"
        )
    return crud.create_user(db=db, user=user)


@app.delete("/user/delete/", tags=["users"])
def delete_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist"
        )
    return crud.delete_user(db=db, db_user=db_user)


@app.get("/home", tags=["articles"])
async def home(db: Session = Depends(get_db)):
    return crud.get_all_articles(db=db)


@app.get("/article/{article_id}", tags=["articles"])
async def article(article_id: int):
    if article_id not in models.fake_articles_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="article doesn't exist"
        )
    return models.fake_articles_db[article_id]


@app.post("/new", tags=["articles"])
async def new(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    db_article = crud.get_article_by_title(db, title=article.title)
    if db_article:
        raise HTTPException(status_code=404, detail="Article already exists")
    return crud.create_article(db=db, article=article)


@app.patch("/edit/{article_id}", tags=["articles"])
async def edit(
    article_id: int, new_article: schemas.ArticleCreate, db: Session = Depends(get_db)
):
    db_article = crud.get_article_by_id(db, id=article_id)
    if not db_article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article doesn't exist"
        )
    return crud.update_article(db=db, article=db_article, new_article=new_article)


@app.delete("/article/delete/", tags=["articles"])
def delete_user(article: schemas.ArticleBase, db: Session = Depends(get_db)):
    db_article = crud.get_article_by_title(db, title=article.title)
    if not db_article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article doesn't exist"
        )
    return crud.delete_article(db=db, db_article=db_article)
