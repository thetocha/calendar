from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from uuid import UUID

from config import jwt_settings
from app.auth.schemas import TokenData
from app.users.models import RoleEnum, GroupRoleEnum
from app.database import get_session
from app.users.crud import UserCrud
from app.group.crud import GroupCrud
from app.users.schemas import GetUser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=jwt_settings.access_token_expire_minutes)
    to_encode.update({"expire": expire.strftime("%Y-%m-%d %H:%M:%S")})

    encoded_jwt = jwt.encode(to_encode, jwt_settings.secret_key, jwt_settings.algorithm)

    return encoded_jwt


def verify_token_access(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, jwt_settings.secret_key, jwt_settings.algorithm)
        user_id: UUID = payload.get("user_id")

        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError as e:
        print(e)
        raise credentials_exception

    return token_data


def get_current_user_details(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not Validate Credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    token = verify_token_access(token, credentials_exception)

    crud = UserCrud(session)
    user = crud.get_user(user_id=token.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_user_group_role(user: GetUser = Depends(get_current_user_details),
                                session: Session = Depends(get_session)):
    crud = GroupCrud(session)
    return crud.get_user_role(user)


def get_current_user_role(user: GetUser = Depends(get_current_user_details)):
    return user.role


def verify_is_administrator(role: RoleEnum = Depends(get_current_user_role)):
    if role is not RoleEnum.ADMINISTRATOR:
        raise HTTPException(status_code=403, detail="You have no rights for this")


def verify_is_not_default_user(role: RoleEnum = Depends(get_current_user_role)):
    if role is RoleEnum.DEFAULT_USER:
        raise HTTPException(status_code=403, detail="You have no rights for this")


def verify_is_not_default_student(role: GroupRoleEnum = Depends(get_current_user_group_role)):
    if role is GroupRoleEnum.DEFAULT_STUDENT:
        raise HTTPException(status_code=403, detail="You have no rights for this")
    return True


def get_current_user_group(user: GetUser = Depends(get_current_user_details),
                           session: Session = Depends(get_session)):
    crud = GroupCrud(session)
    group = crud.get_user_group(user)
    if not group:
        return None
    return group.id
