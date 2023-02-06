from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {'hello': 'world'}

@app.get('/about')
def about():
    return {'data': 'this is going to be mafia app for my dudes in digikala !'}
