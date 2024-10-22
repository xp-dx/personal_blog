from sqlalchemy.orm import Session

from . import models, schemas, database
from .password_hashing import get_password_hash

# Session = sessionmaker(bind=database.engine)
# session = Session()

# c1 = models.User(
#     username="akito",
#     hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
# )


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, db_user: schemas.User):
    db.delete(db_user)
    db.commit()
    return {"message": "Successfully deleted user"}


# session.add(c1)
# # session.add(c2)

# print(session.new)

# session.commit()
