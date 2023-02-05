"""
Модульні тести бази даних
"""
import pytest
from sqlalchemy import text

from app.database.database import Database
from app.tests.config import anyio_backend, precents_evn_variables


@pytest.mark.anyio
@precents_evn_variables
async def test_db_connect():
    """
    Перевірка працездібності бази даних та підключення до неї
    """
    database = Database(test=True)
    async with database.sessionmaker() as session:
        result = await session.scalar(text("SELECT version();"))
        assert isinstance(result, str)
