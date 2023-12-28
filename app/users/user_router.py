from fastapi import APIRouter, HTTPException, Depends
from app.database import get_session
from uuid import UUID
from sqlalchemy.orm import Session

from app.users.crud import UserCrud
from app.users.schemas import CreateUser, GetUser
from app.auth.password_handler import get_hashed_password
from app.auth.token_handler import verify_is_administrator

user_router = APIRouter(tags=["User"])


@user_router.post("/users/", response_model=CreateUser)
def create_user(user: CreateUser, session: Session = Depends(get_session)):
    crud = UserCrud(session)
    db_user = crud.get_user_by_username(username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    user.password = get_hashed_password(user.password)
    return crud.create_user(user=user)


@user_router.get("/users/", response_model=list[GetUser])
def read_users(session: Session = Depends(get_session), skip: int = 0, limit: int = 100):
    crud = UserCrud(session)
    users = crud.get_users(skip=skip, limit=limit)
    return users


@user_router.get("/users/{username}", response_model=GetUser)
def read_user(username: str, session: Session = Depends(get_session)):
    crud = UserCrud(session)
    db_user = crud.get_user_by_username(username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@user_router.put('/update_user', response_model=CreateUser, dependencies=[Depends(verify_is_administrator)])
def update_user(user_details: CreateUser, id_to_update: UUID, session: Session = Depends(get_session)):
    user_details.password = get_hashed_password(user_details.password)
    crud = UserCrud(session)
    crud.update_user(user=user_details, id_to_update=id_to_update)
    return user_details


@user_router.put('/delete_user', response_model=CreateUser, dependencies=[Depends(verify_is_administrator)])
def delete_user(id_to_update: UUID, session: Session = Depends(get_session)):
    crud = UserCrud(session)
    if not crud.get_user(id_to_update):
        raise HTTPException(status_code=404, detail="No such user")
    return crud.delete_user(id_to_update)
