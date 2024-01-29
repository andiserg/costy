"""
Модульні тести бази даних
"""

import pytest
from sqlalchemy import text

from tests.conftest import precents_env_variables  # noqa: F401;


@pytest.mark.asyncio
@precents_env_variables
async def test_db_connect(database):  # noqa: F811;
    """
    Перевірка працездібності бази даних та підключення до неї
    """
    async with database.sessionmaker() as session:
        result = await session.scalar(text("SELECT version();"))
        assert isinstance(result, str)
