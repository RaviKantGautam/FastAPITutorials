from fastapi.applications import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from pydantic import BaseModel, Field
import databases
import sqlalchemy
from typing import List
from datetime import datetime

DATABASE_URL = "sqlite:///./store1.db"

metadata = sqlalchemy.MetaData()

database = databases.Database(DATABASE_URL)

register = sqlalchemy.Table(
    "register",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(500)),
    sqlalchemy.Column("date_created", sqlalchemy.DateTime()),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)

app = FastAPI(title='Async db working')

@app.on_event("startup")
async def connect():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

class RegisterIn(BaseModel):
    name: str = Field(...)

class Register(BaseModel):
    id: int
    name: str
    date_created: datetime

class Message(BaseModel):
    message: str

@app.post('/register/', response_model=Register)
async def create(r: RegisterIn = Depends()):
    query = register.insert().values(
        name=r.name,
        date_created=datetime.utcnow()
    )
    record_id = await database.execute(query)
    query = register.select().where(register.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}

@app.get('/register/{id}', response_model=Register)
async def get_one(id: int):
    query = register.select().where(register.c.id == id)
    row = await database.fetch_one(query)
    return {**row}

@app.get('/register/', response_model=List[Register])
async def get_all():
    query = register.select()
    rows = await database.fetch_all(query)
    return rows

@app.put('/register/{id}', response_model=Register)
async def update(id: int, body: RegisterIn):
    query = register.update().where(register.c.id == id).values(
        name=body.name,
        date_created=datetime.utcnow()
    )
    record_id = await database.execute(query)
    query = register.select().where(register.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}

@app.delete('/register/', response_model=Message)
async def delete(id: int):
    query = register.delete().where(register.c.id==id)
    result = await database.execute(query)
    if result:
        return Message(message='row has been deleted successfully.')
    else:
        raise HTTPException(status_code=404, detail='Data not found')

