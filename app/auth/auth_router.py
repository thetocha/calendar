from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_session
from app.users.crud import UserCrud
from app.auth.password_handler import verify_password
from app.auth.token_handler import create_access_token
from app.auth.token_handler import get_current_user_details
from app.auth.schemas import Token
from app.users.schemas import GetUser, CreateUser
from app.auth.password_handler import get_hashed_password

auth_router = APIRouter(tags=["authentication"])


@auth_router.post("/login", response_model=Token)
def login(user_details: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    crud = UserCrud(session)
    user = crud.get_user_by_username(username=user_details.username)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User does not exist")
    if not verify_password(user_details.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Incorrect password")
    access_token = create_access_token(data={"user_id": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/sign_up", response_model=Token)
def sign_up(user_details: CreateUser, session: Session = Depends(get_session)):
    crud = UserCrud(session)
    user = crud.get_user_by_username(username=user_details.username)

    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already registered")
    user_details.password = get_hashed_password(user_details.password)
    added_user = crud.create_user(user_details)
    access_token = create_access_token(data={"user_id": str(added_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.put('/update_current_user', response_model=CreateUser)
def update_current_user(user_details: CreateUser, user: GetUser = Depends(get_current_user_details),
                        session: Session = Depends(get_session)):
    crud = UserCrud(session)
    user_details.password = get_hashed_password(user_details.password)
    user_details.role = user.role
    crud.update_user(user=user_details, id_to_update=user.id)
    return user


@auth_router.get('/get_current_user', response_model=GetUser)
def get_current_user(user: GetUser = Depends(get_current_user_details)):
    return user
