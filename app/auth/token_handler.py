from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from config import JWTSettings
from app.auth import schemas
from app.database import get_session
from app.users.crud import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')
jwt_settings = JWTSettings()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=jwt_settings.get_minutes)
    to_encode.update({"expire": expire.strftime("%Y-%m-%d %H:%M:%S")})

    encoded_jwt = jwt.encode(to_encode, jwt_settings.get_key, jwt_settings.get_algorithm)

    return encoded_jwt


def verify_token_access(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, jwt_settings.get_key, jwt_settings.get_algorithm)
        username: str = payload.get("username")

        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError as e:
        print(e)
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not Validate Credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    token = verify_token_access(token, credentials_exception)

    user = get_user(username=token.username, session=session)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user
