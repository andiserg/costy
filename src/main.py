"""
Головний файл програми
"""
from fastapi import FastAPI

from src.app.adapters.orm import start_mappers
from src.core.database import Database

database = Database()
get_session = database.get_session_depends
start_mappers()

app = FastAPI()


# Імопрти роутерів нижче ніж створення бази і додатку тому що вони їх імпортують у себе.
# Тому якщо імпорти поставити вище, то буде помилка Cyclic Import Error
from src.routers.auth import router as auth_router  # noqa: E402;
from src.routers.operations import router as operations_router  # noqa: E402;
from src.routers.users import router as users_router  # noqa: E402;

app.include_router(users_router, tags=["users"])
app.include_router(auth_router, tags=["account"])
app.include_router(operations_router, tags=["operations"])
