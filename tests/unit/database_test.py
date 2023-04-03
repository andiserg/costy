"""
Модульні тести бази даних
"""
import pytest
from sqlalchemy import text

# event_loop, database потрібні для правильного функціонування тестів
from tests.config import database, event_loop, precents_evn_variables  # noqa: F401;


@pytest.mark.asyncio
@precents_evn_variables
async def test_db_connect(database):  # noqa: F811;
    """
    Перевірка працездібності бази даних та підключення до неї
    """
    async with database.sessionmaker() as session:
        result = await session.scalar(text("SELECT version();"))
        assert isinstance(result, str)
