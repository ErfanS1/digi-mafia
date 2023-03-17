import datetime
from typing import Optional
from database.enums import GameStatus
from Users.schemas import UserView
from pydantic import BaseModel

from database.enums import Team


class Game(BaseModel):
    players: dict
    roles: dict
    creator_id: int
    created_at: datetime.datetime
    started_at: Optional[datetime.datetime]
    status: GameStatus
    creator: UserView

    class Config:
        orm_mode = True

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
