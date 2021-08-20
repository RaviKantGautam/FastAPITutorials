from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

class Package(BaseModel):
    name: str
    number: int
    description: Optional[str] = None

class PackageIN(BaseModel):
    secret_id: str
    name: str
    number: int
    description: Optional[str] = None


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

@app.post("/package/{my_id}") # body response data oon POST request
async def make_package(my_id: int,pack: Package):
    return {"id": my_id, **pack.dict()}


@app.post("/packagesecret/{my_id}", response_model=Package) # This is to hide secret data/variable
async def make_package_secret(my_id: int,pack: PackageIN):
    return {"id": my_id, **pack.dict()}


@app.post("/packagesecretexclude/{my_id}", response_model=Package, response_model_exclude=('description',)) # This is to remove the optional fields
async def make_package_secret_exclude(my_id: int,pack: PackageIN):
    return {"id": my_id, **pack.dict()}

@app.post("/packagesecretinclude/{my_id}", response_model=Package, response_model_include=('description',)) # This is to include only the specific fields
async def make_package_secret_include(my_id: int,pack: PackageIN):
    return {"id": my_id, **pack.dict()}