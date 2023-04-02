from typing import List, Union

from pydantic import BaseModel


class User(BaseModel):
    username: str
    fullname: str
    password: str
    email: str

    class Config:
        orm_mode = True


class UserMetaData(BaseModel):
    user_id: int
    rank: int
    games_played: int
    games_abandoned: int

    class Config:
        orm_mode = True


class UserView(BaseModel):
    username: str
    email: str
    metadatas: List[UserMetaData] = []

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None


class AllUsers(BaseModel):
    users: List[UserView]
    currentUser: UserView
