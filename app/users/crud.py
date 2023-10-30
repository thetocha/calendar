from sqlalchemy.orm import Session

from .models import User
from .schemas import CreateUser


def get_user(db: Session, user_name: str):
    return db.query(User).filter(User.username == user_name).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: CreateUser):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    return db_user
