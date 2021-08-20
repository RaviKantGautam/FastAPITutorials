from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def hello():
    return {"context": "Hello World"}

@app.get('/component/{id}') # path parameter 
async def get_componenet(id: int):
    return {"id": id}

@app.get('/component/') # query parameter /component/?id=2&text=Hello world
async def get_read(id: int, text: str):
    return {"id": id, "text": text}