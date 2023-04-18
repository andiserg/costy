"""
Фікстури і інші структури, які використовуються у тестах
"""
import asyncio
import os

import pytest
import pytest_asyncio
from httpx import AsyncClient

from src.database import Database, DatabaseFactory
from src.main import bootstrap_fastapi_app


@pytest.fixture(scope="session")
def event_loop():
    """
    Фікстура потрібна для функціонування pytest-asyncio тестів
    """
    return asyncio.get_event_loop()


# Декоратор-перевірка на те, чи існує файл "pytest.ini"
# або існують потрібні ENV параметри
# Перевірка для того, щоб тести не крашились якщо не має потрібних env параметрів.
precents_evn_variables = pytest.mark.skipif(
    all(
        [
            # Якщо результат буде True то тест пропуститься.
            # Тому перед умовами добавлені not
            not os.path.exists("pytest.ini"),
            not all(
                [
                    os.getenv(key, False)
                    for key in ["DB_USER", "DB_PASSWORD", "DB_HOST", "TEST_DB_NAME"]
                ]
            ),
        ]
    ),
    reason="Missing env variables",
)


@pytest.fixture(scope="session")
def database_factory() -> DatabaseFactory:
    return DatabaseFactory()


@pytest_asyncio.fixture
async def database(database_factory) -> Database:
    """
    Фікстура яка створює об'єкт Database для модульних тестів
    :return: Database object
    """
    db = database_factory.get_database(test=True)
    await db.init_models()
    return db


@pytest_asyncio.fixture
async def client_db(database_factory) -> AsyncClient:  # noqa: F401, F811;
    """
    Створює і повертає httpx.AsyncClient зі створеною тестовою базою
    :return: httpx.AsyncClient
    """
    async with AsyncClient(
        app=bootstrap_fastapi_app(database_factory, test=True),
        base_url="http://127.0.0.1:8000",
    ) as session:
        # yield для того, щоб після тесту відбулоась "чистка" фікстури.
        # В цьому випадку це вихід з контекстного менеджера, який закриє клієнт
        yield session
