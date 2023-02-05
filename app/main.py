"""
Головний файл програми
"""
from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import Database

database = Database()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/database_info/")
async def say_db_verion(session: AsyncSession = Depends(database.get_session_depends)):
    return {"message": await session.scalar(text("SELECT version();"))}
