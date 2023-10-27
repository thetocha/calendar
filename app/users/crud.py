from sqlalchemy.orm import Session

from app.users import models, schemas


def get_user(db: Session, user_name: str):
    return db.query(models.User).filter(models.User.user_name == user_name).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.CreateUser):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    return db_user
