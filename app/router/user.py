from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any
from app.Users import schemas
from app.database.database import get_db
from app.database import db_models
from sqlalchemy.orm import Session
from app.Authentication.hashing import Hash
from app.Authentication import oauth2

router = APIRouter(
    prefix='/users',
    tags=['Users'],
)

@router.get('/all')
def get_all_users(db: Session = Depends(get_db), currentUser: db_models.User = Depends(oauth2.getCurrentUser)) -> Any:
    users = db.query(db_models.User).all()

    allUsers = schemas.AllUsers(users=users, currentUser=currentUser)
    return allUsers

@router.get('/{id}', status_code=200, response_model=schemas.UserView)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(db_models.User).filter(db_models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=405, detail=f'user {id} not found')
    return user


@router.post('/delete/{id}', status_code=status.HTTP_200_OK)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(db_models.User).filter(db_models.User.id == id).delete(synchronize_session=False)

    return {'user deleted': 'done'}

@router.put('/update/{id}', status_code=status.HTTP_201_CREATED)
def update_user(id: int, user: schemas.User, db: Session = Depends(get_db)):
    oldUser = db.query(db_models.User).filter(db_models.User.id == id).first()
    if not oldUser:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        db.query(db_models.User).filter(db_models.User.id == id).update(user.dict())

    db.commit()
    db.refresh(oldUser)

    return oldUser


@router.post('/create-user', response_model=schemas.UserView, tags=['Users'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    user = db_models.User(
        username=request.username,
        fullname=request.fullname,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.post('/user/add-info/{id}', response_model=schemas.UserView)
def add_info(metadata: schemas.UserMetaData, id: int, db: Session = Depends(get_db)):
    user = db.query(db_models.User).filter(db_models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=405, detail=f'user {id} not found')

    userMetaData = db.query(db_models.UserMetaData).filter(db_models.UserMetaData.user_id == id).first()
    if userMetaData:
        userMetaData.user_id = id
        userMetaData.rank = metadata.rank
    else:
        userMetaData = db_models.UserMetaData(user_id=id, rank=metadata.rank)
        db.add(userMetaData)

    db.commit()

    return user

@router.get('/user-info/{id}', response_model=schemas.UserMetaData)
def get_user_metadata(id: int, db: Session = Depends(get_db)):
    userMetaData = db.query(db_models.UserMetaData).filter(db_models.UserMetaData.id == id).first()

    return userMetaData
