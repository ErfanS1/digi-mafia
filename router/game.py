from fastapi import APIRouter, Depends, HTTPException
from database.database import get_db
from database import db_models
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/game',
    tags=['Game'],
)


@router.post('/')
def createGame(request, db: Session = Depends(get_db)):
    game = db_models.Game(
        # creator_id=3,
        players={'asd': 'asw'},
    )
    db.add(game)
    db.commit()

    return game
