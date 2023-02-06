"""
Головний файл програми
"""
from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import Database

database = Database()
get_session = database.get_session_depends

app = FastAPI()

# Імопрти роутерів нижче ніж створення бази і додатку тому що вони їх імпортують у себе.
# Тому якщо імпорти поставити вище, то буде помилка Cyclic Import Error
from app.views.users import router as users_router  # noqa: E402;

app.include_router(users_router, tags=["users"])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/database_info/")
async def say_db_verion(session: AsyncSession = Depends(database.get_session_depends)):
    return {"message": await session.scalar(text("SELECT version();"))}
