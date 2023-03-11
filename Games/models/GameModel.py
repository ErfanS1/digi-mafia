from database import db_models
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified

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


    def startGame(self, game):
        pass
