from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from Authentication.token import getOptionalUserFromToken, getUserFromToken
from database import db_models
from database.database import get_db
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)


async def getOptionalCurrentUser(
        token: str = Depends(oauth2_scheme), 
        db: Session = Depends(get_db)
) -> Optional[db_models.User]:
    
    return getOptionalUserFromToken(token, db)


async def getCurrentUser(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> db_models.User:
    
    return getUserFromToken(token, db)
