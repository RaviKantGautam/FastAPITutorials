from fastapi import FastAPI, HTTPException
from typing import Optional, List
from pydantic import BaseModel

class TodoConstruct(BaseModel):
    name: str
    description: Optional[str]

app = FastAPI(title="Todo App")

store_todos = list()

@app.get('/', response_model=List[TodoConstruct])
async def home():
    return store_todos

@app.post('/todo/', response_model=TodoConstruct)
async def create_todo(todo: TodoConstruct):
    store_todos.append(todo)
    return todo

@app.put('/todo/', response_model=TodoConstruct)
async def update_todo(id:int,todo: TodoConstruct):
    try:
        store_todos[id] = todo
        return store_todos[id]
    except Exception:
        raise HTTPException(status_code=404, detail="Todo not found")

@app.delete('/todo/')
async def delete_todo(id:int):
    try:
        del store_todos[id]
        return {"status": 200, "message": 'Item deleted successfully.'}
    except Exception:
        raise HTTPException(status_code=404, detail="Todo not found")
