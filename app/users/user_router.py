from fastapi import APIRouter, HTTPException, Depends
from app.database import get_session
from sqlalchemy.orm import Session

from app.users import crud
from app.users.schemas import CreateUser, GetUser
from app.auth.password_handler import get_hashed_password

user_router = APIRouter(tags=["User"])


@user_router.post("/users/", response_model=CreateUser)
def create_user(user: CreateUser, session: Session = Depends(get_session)):
    db_user = crud.get_user_by_username(session=session, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    user.password = get_hashed_password(user.password)
    return crud.create_user(user=user, session=session)


@user_router.get("/users/", response_model=list[GetUser])
def read_users(session: Session = Depends(get_session), skip: int = 0, limit: int = 100):
    users = crud.get_users(session, skip=skip, limit=limit)
    return users


@user_router.get("/users/{username}", response_model=GetUser)
def read_user(username: str, session: Session = Depends(get_session)):
    db_user = crud.get_user_by_username(username=username, session=session)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
