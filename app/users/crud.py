from sqlalchemy.orm import Session
from app.users.models import User
from app.users.schemas import CreateUser

from uuid import UUID


def get_user(username: str, session: Session):
    return session.query(User).filter(User.username == username).first()


def get_users(session: Session, skip: int = 0, limit: int = 100):
    return session.query(User).offset(skip).limit(limit).all()


def create_user(user: CreateUser, session: Session):
    user_to_add = User(**user.dict())
    session.add(user_to_add)
    session.commit()
    return user_to_add


def update_user(user: CreateUser, session: Session, id_to_update: UUID):
    user_to_update = session.query(User).filter(User.id == id_to_update).first()
    if user_to_update is None:
        return None
    user_to_update.update(**user.dict())
    session.commit()
    return user_to_update
