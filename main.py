from fastapi import Depends
from sqlalchemy import select

from app_factory import app_factory
from db import get_db
from models import Todo

app = app_factory()


@app.get("/ping", status_code=200)
async def ping():
    return {"message": "pong"}


@app.get("/todo")
async def get_todo(session=Depends(get_db)):
    query = select(Todo)
    result = await session.execute(query)
    tasks = [item.task for item in result.scalars()]
    return {"tasks": tasks}
