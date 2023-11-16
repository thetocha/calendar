from sqlalchemy.orm import Session
from app.users.models import User
from app.users.schemas import CreateUser

from uuid import UUID


def get_user_by_username(username: str, session: Session):
    return session.query(User).filter(User.username == username).first()


def get_user(user_id: UUID, session: Session):
    return session.query(User).filter(User.id == user_id).first()


def get_users(session: Session, skip: int = 0, limit: int = 100):
    return session.query(User).offset(skip).limit(limit).all()


def create_user(user: CreateUser, session: Session):
    user_to_add = User(**user.dict())
    session.add(user_to_add)
    session.commit()
    return user_to_add


def update_user(user: CreateUser, session: Session, id_to_update: UUID):
    update_query = session.query(User).filter(User.id == id_to_update)
    user_to_update = update_query.first()
    if user_to_update is None:
        return None
    info = {"id": user_to_update.id}
    info.update(**user.dict())
    update_query.update(info)
    session.commit()
    return user_to_update
