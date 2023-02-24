from typing import Union
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status
from Users.schemas import UserView
from repositories import usersRepository
from sqlalchemy.orm import Session


SECRET_KEY = "1a58606a625cab0a54e24d4bc33eaeeb47cead8c1dc05d4952d11c1a606a0791"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    to_encode['exp'] = expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def getUserFromToken(token: str, credentials_exception: HTTPException, db: Session) -> UserView:
    print(11)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = usersRepository.getUserWithEmail(email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user
