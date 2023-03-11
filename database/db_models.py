import datetime
import time

from .enums import Team, GameStatus
from sqlalchemy import Column, Integer, String, JSON, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy.sql import func

from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    fullname = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column('rolee', Enum('user', 'admin', name='roleEnum'), default='user')

    metadatas = relationship('UserMetaData', back_populates='user')

class UserMetaData(Base):
    __tablename__ = 'users_metadata'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    rank = Column(Integer, default=0)
    games_played = Column(Integer, default=0)
    games_abandoned = Column(Integer, default=0)

    user = relationship('User', back_populates='metadatas')

class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True, autoincrement=True)
    creator_id = Column(Integer, ForeignKey('users.id'))
    players = Column(JSONB, default=dict)
    roles = Column(JSONB, default=dict)
    status = Column(Enum(GameStatus), default=GameStatus.New, nullable=False)
    winners_team = Column(Enum(Team))
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.now)
    started_at = Column(DateTime(timezone=True))
    ended_at = Column(DateTime(timezone=True))
#
# class ActionsPerGame(Base):
#     __tablename__ = 'actions_per_games'
#     id = Column(Integer, primary_key=True, index=True)
#     game_id = Column(Integer)
#     player_id = Column(Integer)
#     result = Column(Enum)
#     type = Column(Enum)

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    side = Column(Enum(Team), nullable=False)
    creator_id = Column(Integer, ForeignKey('users.id'))
    description = Column(String)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.now)


# naghsh tedad, add e naghsh, pakhsh e naghsh, random,  add e esm, random assign ba repeat
