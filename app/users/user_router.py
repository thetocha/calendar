from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.users import crud
from app.users.schemas import CreateUser, GetUser

router = APIRouter()


@router.post("/users/", response_model=CreateUser)
def create_user(user: CreateUser, session: Session):
    db_user = crud.get_user(session=session, user_name=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(user=user, session=session)


@router.get("/users/", response_model=list[GetUser])
def read_users(session: Session, skip: int = 0, limit: int = 100):
    users = crud.get_users(session, skip=skip, limit=limit)
    return users


@router.get("/users/{user_name}", response_model=GetUser)
def read_user(user_name: str, session: Session):
    db_user = crud.get_user(user_name=user_name, session=session)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
