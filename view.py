from mymodel import Todo, TodoIn_Pydantic, Todo_Pydantic
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise, HTTPNotFoundError
from typing import List

class Message(BaseModel):
    message: str


app = FastAPI(title='Todo model')

@app.get('/')
async def home():
    return {"context": "Welcome to home page."}

@app.get('/todos/', response_model=List[Todo_Pydantic])
async def get_todos():
    return await Todo_Pydantic.from_queryset(Todo.all())


@app.get('/todo/{id}', response_model=Todo_Pydantic, responses={"404": {"model": HTTPNotFoundError}})
async def get_todo(id: int):
    return await Todo_Pydantic.from_queryset_single(Todo.get(id=id))


@app.post('/todo/', response_model=Todo_Pydantic, responses={"404": {"model": HTTPNotFoundError}})
async def create(todo: TodoIn_Pydantic):
    response = await Todo.create(**todo.dict(exclude_unset=True))
    return await Todo_Pydantic.from_tortoise_orm(response)


@app.put('/todo/{id}', response_model=Todo_Pydantic, responses={"404": {"model": HTTPNotFoundError}})
async def update(id:int, todo: TodoIn_Pydantic):
    await Todo.filter(id=id).update(**todo.dict(exclude_unset=True))
    return await Todo_Pydantic.from_queryset_single(Todo.get(id=id))
   

@app.delete('/todo/{id}', response_model=Message, responses={"404": {"model": HTTPNotFoundError}})
async def delete(id:int):
    deleted_count = await Todo.filter(id=id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail='Todo not found')
    return Message(message='Todo deleted successfully')
   

   
# connecting database
register_tortoise(
    app,
    db_url='sqlite://store.db',
    modules={'models': ['mymodel']},
    generate_schemas=True,
    add_exception_handlers=True,
)