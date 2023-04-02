from fastapi import FastAPI
from app.database import db_models
from app.database.database import engine
from app.router import user, game, authentication
import uvicorn

app = FastAPI()

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(game.router)

db_models.Base.metadata.create_all(bind=engine)

@app.get('/')
def index():
    return {'data': 'almost there..'}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
