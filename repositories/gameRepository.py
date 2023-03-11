from typing import Optional

from Games import schemas
from database import enums
from database import db_models
from .repository import Repository


class GameRepository(Repository):
    def __init__(self, db):
        super().__init__(db)
        self.dbModel = db_models.Game

    def getNewGameByCreatorId(self, creator_id: int) -> Optional[db_models.Game]:
        game = self.db.query(self.dbModel)\
            .filter(db_models.Game.creator_id == creator_id and db_models.Game.status == enums.GameStatus.New)\
            .one_or_none()

        # print('gameId', game.id)

        return game

    def createGame(self, creator_id: int):
        game = self.dbModel(
            creator_id=creator_id
        )
        self.db.add(game)
        self.db.commit()
        self.db.refresh(game)

        return game

    # def addPlayerToGame(self, game_id: int, players: dict) -> db_models.Game:
    #     self.db.query(db_models.Game).filter(db_models.Game.id == game_id).update({'players': players})
    #     self.db.commit()
    #     # self.db.refresh()
    #     return None

    def createRole(self, role: schemas.Role, creator_id: int):
        role = db_models.Role(
            title=role.title,
            side=role.side,
            creator_id=creator_id,
            description=role.description,
        )

        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)

        return role



