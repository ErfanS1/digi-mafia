# import datetime
from database import db_models
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from ..exceptions import ValidateException
from random import shuffle
from database.enums import GameStatus
from datetime import datetime


class GameModel:
    def addRoleToGame(self, role: db_models.Role, game: db_models.Game, db: Session):
        role_key = str(role.id)
        if role_key in game.roles:
            game.roles[role_key]['quantity'] += 1
        else:
            game.roles[role_key] = {
                'id': role.id,
                'title': role.title,
                'quantity': 1,
                'player': None,
                'player_id': None,
            }

        flag_modified(game, 'roles')
        db.flush()
        db.commit()

    def startGame(self, game: db_models.Game, db: Session):
        playersCount = len(game.players)
        roleCount = self.calculateRolesCount(game.roles)
        if playersCount != roleCount:
            raise ValidateException('number of roles not equal to number of players!')

        roles = []
        for role_id in game.roles:
            roleDetail = game.roles[role_id]
            quantity = roleDetail['quantity']
            for i in range(quantity):
                roles.append((roleDetail['id'], roleDetail['title']))

        shuffle(roles)

        role_ptr = 0
        for player in game.players:
            game.players[player]['role'] = {
                'id': roles[role_ptr][0],
                'title': roles[role_ptr][1],
            }
            role_ptr += 1

        game.status = GameStatus.Started
        game.started_at = datetime.now()
        flag_modified(game, 'players')
        db.flush()
        db.commit()

        return game

    def calculateRolesCount(self, roles: dict):
        count = 0
        for role_id in roles:
            count += roles[role_id]['quantity']

        return count
