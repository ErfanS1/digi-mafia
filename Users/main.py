from typing import List, Any

from fastapi import FastAPI, Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from . import schemas, models
from .database import engine, SessionLocal
from Authentication.hashing import Hash

app = FastAPI()

router = APIRouter()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.post('/add-user')
# def addUser(user: schemas.User, db: Session = Depends(get_db)):
#     newUser = models.User(first_name=user.firstname, last_name=user.last_name)
#     firstId = newUser.id
#     db.add(newUser)
#     afterAddId = newUser.id
#     db.commit()
# db.refresh(newUser)

# return {'fn': newUser.first_name,
#         'ln': newUser.last_name,
#         'id': newUser.id,
#         'fid': firstId,
#         'aaid': afterAddId
#         }


@app.get('/users', response_model=List[schemas.User], tags=['Users'])
def getAllUsers(db: Session = Depends(get_db)) -> Any:
    users = db.query(models.User).all()
    return users


@app.get('/user/{id}', status_code=200, response_model=schemas.UserView, tags=['Users'])
def getUser(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=405, detail=f'user {id} not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail':f'user {id} not found'}
    return user


@app.post('/user/delete/{id}', status_code=status.HTTP_200_OK, tags=['Users'])
def deleteUser(id: int, db: Session = Depends((get_db))):
    user = db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
    # db.commit()
    # user = db.query(models.User).filter(models.User.id == id).first()
    # db.delete(user)
    # db.commit()
    return {'user deleted': 'done'}


@app.put('/user/update/{id}', status_code=status.HTTP_201_CREATED, tags=['Users'])
def updateUser(id: int, user: schemas.User, db: Session = Depends(get_db)):
    # user = models.User(first_name=user.name, last_name=user.role)
    # db.query(models.User).filter(models.User.id == id).update(user)
    # oldUser = db.query(models.User).filter(models.User.id == id).first()
    # print(oldUser)
    # if not oldUser:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    # else:
    #     db.query(models.User).filter(models.User.id == id).update(user.dict(), synchronize_session=False)

    oldUser = db.query(models.User).filter(models.User.id == id)
    if not oldUser.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    else:
        oldUser.update(user.dict())

    db.commit()

    # sql = "select * from users"
    # users = db.query(models.User).where(models.User.id > 2).all()
    # print(oldUser, user)
    return oldUser
    # return users
    # return 'done'


@app.post('/create-user', response_model=schemas.UserView, tags=['Users'])
def createUser(user: schemas.User, db: Session = Depends(get_db)):
    user = models.User(
        username=user.username,
        fullname=user.fullname,
        email=user.email,
        password=Hash.bcrypt(user.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@app.post('/user/add-info/{id}', response_model=schemas.UserView)
def addInfo(metadata: schemas.UserMetaData, id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=405, detail=f'user {id} not found')

    userMetaData = db.query(models.UserMetaData).filter(models.UserMetaData.user_id == id).first()
    print(userMetaData)
    if userMetaData:
        userMetaData.update(metadata.dict())
    else:
        userMetaData = models.UserMetaData(user_id=id, rank=metadata.rank)
        db.add(userMetaData)

    db.commit()

    return user

@app.get('/user-info/{id}', response_model=schemas.UserMetaData)
def getUserMetaData(id: int, db: Session = Depends(get_db)):
    userMetaData = db.query(models.UserMetaData).filter(models.UserMetaData.id == id).first()
    print(userMetaData)
    return userMetaData


