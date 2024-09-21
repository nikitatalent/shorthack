
from fastapi import FastAPI, Depends
from pydantic import BaseModel, ConfigDict

app = FastAPI()


@app.get("/")
async def home():
    return {"data": "Hello World"}


class STaskAdd(BaseModel):
   name: str
   description: (str or None) = None


@app.post("/")
async def add_task(task: STaskAdd = Depends()):
   return {"data": task}


class STask(STaskAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)

