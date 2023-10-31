from fastapi import Depends

from app.database import get_session
from app.users.models import User
from app.users.schemas import CreateUser


def get_user(user_name: str, session: Depends(get_session)):
    return session.query(User).filter(User.username == user_name).first()


def get_users(session: Depends(get_session), skip: int = 0, limit: int = 100):
    return session.query(User).offset(skip).limit(limit).all()


def create_user(user: CreateUser, session: Depends(get_session)):
    user_to_add = User(**user.dict())
    session.add(user_to_add)
    session.commit()
    return user_to_add
