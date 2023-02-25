from fastapi import FastAPI

from Users import models
from database.database import engine
from router import user, authentication
import uvicorn

app = FastAPI()

app.include_router(authentication.router)
app.include_router(user.router)

models.Base.metadata.create_all(bind=engine)

@app.get('/')
def index():
    return {'hello': 'world'}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)