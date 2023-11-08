from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_session
from app.users.crud import get_user, create_user, update_user
from app.auth.password_handler import verify_password
from app.auth.token_handler import create_access_token
from app.auth.token_handler import get_current_user
from app.auth.schemas import Token
from app.users.schemas import GetUser, CreateUser

auth_router = APIRouter(tags=["authentication"])


@auth_router.post("/login", response_model=Token)
def login(user_details: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = get_user(username=user_details.username, session=session)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User does not exist")
    if not verify_password(user_details.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Incorrect password")
    access_token = create_access_token(data={"username": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/sing_up", response_model=Token)
def sing_up(user_details: CreateUser, session: Session = Depends(get_session)):
    user = get_user(username=user_details.username, session=session)

    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already registered")
    create_user(user, session)
    access_token = create_access_token(data={"username": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.put('/me', response_model=CreateUser)
def get_me(user_details: CreateUser, user: GetUser = Depends(get_current_user),
           session: Session = Depends(get_session)):
    update_user(user=user_details, session=session, id_to_update=user.id)
    return user
