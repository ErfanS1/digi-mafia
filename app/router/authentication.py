from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from app.Authentication.hashing import Hash
from app.Authentication.token import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.database.database import get_db
from app.database import db_models
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)

@router.post('/login')
def login(formData: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(db_models.User).filter(db_models.User.email == formData.username).first()
    if not user:
        raise HTTPException(status_code=404, detail='not found')

    if Hash.verify(formData.password, user.password):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=404, detail='not found')
