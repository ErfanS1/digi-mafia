from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()


@app.get('/')
def index():
    return {'hello': 'world'}


@app.get('/about')
def about():
    return {'data': 'this is going to be mafia app for my dudes in digikala !'}


@app.get('/player/{id}')
def getPlayerData(id: int, ss: Optional[bool] = 'sd'):
    player = ['erf', 'ali']
    return {
        'id': id,
        'player-name': player[int(id)],
        'ss': ss,
    }


class player(BaseModel):
    name: Optional[str]
    role: Optional[str] = 'saade'
    points: Optional[int]
@app.post('/add/player')
def addPlayer(player: Optional[player]):
    # player = 10
    return {
        'id': 10,
        'name': player.name if player else 'bikhial',
        'role': player.role if player else 'bikhial',
        'pts': player.points if player else 'vel kon'
    }

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)