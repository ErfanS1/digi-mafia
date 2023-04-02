from fastapi import APIRouter, Depends, HTTPException, status
from app.Authentication import oauth2
from app.Games import schemas
from app.Games.models.GameModel import GameModel
from app.Games.schemas import ShowRole
from app.database.database import get_db
from app.database import db_models
from sqlalchemy.orm import Session
from app.repositories.gameRepository import GameRepository
from app.repositories.roleRepository import RoleRepository
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.exc import IntegrityError
from typing import List
from app.Games.exceptions import ValidateException


router = APIRouter(
    prefix='/game',
    tags=['Game'],
)


@router.post('/')
def create_game(
        db: Session = Depends(get_db),
        currentUser: db_models.User = Depends(oauth2.getCurrentUser)
):
    gameRepository = GameRepository(db)
    game = gameRepository.getNewGameByCreatorId(currentUser.id)

    if game:
        return game

    game = gameRepository.createGame(currentUser.id)
    return game

@router.post('/add/player-nn')
def add_player_nickname(
        nickName: schemas.NickName,
        db: Session = Depends(get_db),
        currentUser: db_models.User = Depends(oauth2.getCurrentUser)
):
    user_id = currentUser.id
    gameRepository = GameRepository(db)
    game = gameRepository.getNewGameByCreatorId(user_id)

    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if nickName.name in game.players:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='name already existed')

    game.players[nickName.name] = {'name': nickName.name, 'role': None}
    flag_modified(game, 'players')
    db.flush()
    db.commit()

    return game

@router.post('/add/role')
def add_role(
        role: schemas.Role,
        db: Session = Depends(get_db),
        currentUser: db_models.User = Depends(oauth2.getCurrentUser)
) -> schemas.Role:
    gameRepository = GameRepository(db)
    try:
        role = gameRepository.createRole(role, currentUser.id)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='title already existed')

    return role

@router.post('/add/role/{role_id}')
def add_role_to_game(
        role_id: int,
        db: Session = Depends(get_db),
        currentUser: db_models.User = Depends(oauth2.getCurrentUser)
):
    gameRepository = GameRepository(db)
    game = gameRepository.getNewGameByCreatorId(currentUser.id)

    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    role = RoleRepository(db).getById(role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    GameModel().addRoleToGame(role, game, db)

    return game.roles

@router.get('/roles')
def get_all_roles(db: Session = Depends(get_db)) -> List[ShowRole]:
    roleRepository = RoleRepository(db)
    roles = roleRepository.getAll()

    return roles

@router.post('/start')
def start_game(
        db: Session = Depends(get_db),
        currentUser: db_models.User = Depends(oauth2.getCurrentUser),
):
    game = GameRepository(db).getNewGameByCreatorId(currentUser.id)
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    try:
        GameModel().startGame(game, db)
    except ValidateException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    return game

@router.get('/{id}')
def get_game(
        game_id: int,
        db: Session = Depends(get_db),
        currentUser: db_models.User = Depends(oauth2.getCurrentUser),
) -> schemas.Game:
    game = GameRepository(db).getById(game_id)
    if not game or game.creator_id != currentUser.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return game

