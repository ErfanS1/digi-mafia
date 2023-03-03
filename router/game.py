from typing import Optional
from fastapi import APIRouter, Depends
from Authentication import oauth2
from database.database import get_db
from database import db_models
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/game',
    tags=['Game'],
)


@router.post('/')
def createGame(
        db: Session = Depends(get_db),
        currentUser: Optional[db_models.User] = Depends(oauth2.getOptionalCurrentUser)
):
    user_id = currentUser.id if currentUser else None
    game = db_models.Game(
        creator_id=user_id
    )
    db.add(game)
    db.commit()

    return game
