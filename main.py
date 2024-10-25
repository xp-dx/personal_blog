from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from . import models, schemas, crud, config
from datetime import timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError
from jinja2 import Template


app = FastAPI(title="Personal Blog")
templates = Jinja2Templates(directory="./personal_blog/templates")


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
    db: Session = Depends(get_db),
) -> schemas.Token:
    user = crud.authenticate_user(
        db=db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(config.ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)

    except InvalidTokenError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
    current_user: Annotated[schemas.User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


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
def delete_user(
    current_user: Annotated[schemas.Admin, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_user = crud.get_user_by_username(db, username=current_user.username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist"
        )
    return crud.delete_user(db=db, db_user=db_user)


@app.get("/home", tags=["articles"])
async def home(request: Request, db: Session = Depends(get_db)):
    articles = crud.get_all_articles(db=db)
    return templates.TemplateResponse(
        "home.html", {"request": request, "articles": articles}
    )


# @app.get("/home", tags=["articles"])
# async def home(db: Session = Depends(get_db)):
#     articles = crud.get_all_articles(db=db)
#     template = Template(
#         open(
#             "/home/akito/code/pet_projects/personal_blog/templates/home.html", "r"
#         ).read()
#     )
#     html_content = template.render(articles=articles)
#     return HTMLResponse(content=html_content, status_code=200)


# @app.get("/home", tags=["articles"])
# async def home(db: Session = Depends(get_db)):
#     return crud.get_all_articles(db=db)


@app.get("/article/{article_id}", tags=["articles"])
async def article(article_id: int):
    if article_id not in models.fake_articles_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="article doesn't exist"
        )
    return models.fake_articles_db[article_id]


@app.post("/new", tags=["articles"])
async def new(
    article: schemas.ArticleCreate,
    current_user: Annotated[schemas.Admin, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    db_article = crud.get_article_by_title(db, title=article.title)
    if db_article:
        raise HTTPException(status_code=404, detail="Article already exists")
    return crud.create_article(db=db, article=article)


@app.patch("/edit/{article_id}", tags=["articles"])
async def edit(
    article_id: int,
    new_article: schemas.ArticleCreate,
    current_user: Annotated[schemas.Admin, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    db_article = crud.get_article_by_id(db, id=article_id)
    if not db_article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article doesn't exist"
        )
    return crud.update_article(db=db, article=db_article, new_article=new_article)


@app.delete("/delete/{article_id}/", tags=["articles"])
def delete_user(
    article_id: int,
    current_user: Annotated[schemas.Admin, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    db_article = crud.get_article_by_id(db, id=article_id)
    if not db_article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article doesn't exist"
        )
    return crud.delete_article(db=db, db_article=db_article)


@app.get("/users/me/", response_model=schemas.Admin)
async def read_users_me(
    current_user: Annotated[schemas.User, Depends(get_current_user)],
):
    return current_user
