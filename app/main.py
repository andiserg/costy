"""
Головний файл програми
"""
from fastapi import FastAPI

from app.database.database import Database

database = Database()
get_session = database.get_session_depends

app = FastAPI()

from app.views.auth import router as auth_router  # noqa: E402;

# Імопрти роутерів нижче ніж створення бази і додатку тому що вони їх імпортують у себе.
# Тому якщо імпорти поставити вище, то буде помилка Cyclic Import Error
from app.views.users import router as users_router  # noqa: E402;

app.include_router(users_router, tags=["users"])
app.include_router(auth_router, tags=["auth"])
