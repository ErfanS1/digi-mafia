from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from Authentication.token import getUserFromToken
from database.database import get_db
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def getCurrentUser(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return getUserFromToken(token, credentials_exception, db)
