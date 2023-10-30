from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_session

from . import crud
from .schemas import CreateUser, GetUser

router = APIRouter()


@router.post("/users/", response_model=CreateUser)
def create_user(user: CreateUser, session: Session = Depends(get_session)):
    db_user = crud.get_user(session, user_name=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Login already registered")
    return crud.create_user(db=session, user=user)


@router.get("/users/", response_model=list[GetUser])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_name}", response_model=GetUser)
def read_user(user_name: str, db: Session = Depends(get_session)):
    db_user = crud.get_user(db, user_name=user_name)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
