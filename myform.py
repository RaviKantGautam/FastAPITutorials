from fastapi import FastAPI, Form

app = FastAPI(title="Form Practice")

@app.post('/createform/')
async def createform(name: str = Form(...), type: str = Form(...)):
    return {'name': name, 'type': type}