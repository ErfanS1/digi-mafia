from typing import List, Union

from pydantic import BaseModel

from database.enums import Team


class Game(BaseModel):
    pass
    # username: str
    # fullname: str
    # password: str
    # email: str
    #
    # class Config:
    #     orm_mode = True

class NickName(BaseModel):
    name: str


class Role(BaseModel):
    title: str
    side: Team
    description: str

    class Config:
        orm_mode = True

class ShowRole(Role):
    id: int
