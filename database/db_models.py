import enum

from sqlalchemy import Column, Integer, String, JSON, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship

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


class Teams(enum.Enum):
    Citizens = 'Citizens'
    Mafia = 'Mafia'
class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey('users.id'))
    players = Column(JSON)
    winners_team = Column(Enum(Teams))
    # created_at = Column(DateTime)
    # started_at = Column(DateTime)
    # ended_at = Column(DateTime)
#
#
# class ActionsPerGame(Base):
#     __tablename__ = 'actions_per_games'
#     id = Column(Integer, primary_key=True, index=True)
#     game_id = Column(Integer)
#     player_id = Column(Integer)
#     result = Column(Enum)
#     type = Column(Enum)
#
