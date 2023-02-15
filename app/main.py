"""
Головний файл програми
"""
from fastapi import FastAPI

from app.core.database import Database

database = Database()
get_session = database.get_session_depends

app = FastAPI()


# Імопрти роутерів нижче ніж створення бази і додатку тому що вони їх імпортують у себе.
# Тому якщо імпорти поставити вище, то буде помилка Cyclic Import Error
from app.auth.views import router as auth_router  # noqa: E402;
from app.views.operations import router as operations_router  # noqa: E402;
from app.views.users import router as users_router  # noqa: E402;

app.include_router(users_router, tags=["users"])
app.include_router(auth_router, tags=["auth"])
app.include_router(operations_router, tags=["operations"])
