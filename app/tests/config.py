"""
Фікстури і інші структури, які використовуються у тестах
"""
import asyncio
import os

import pytest
import pytest_asyncio
from httpx import AsyncClient

from app.database.database import Database
from app.main import app

# from app.main import database as default_database


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


@pytest_asyncio.fixture
async def database() -> Database:
    """
    Фікстура яка створює об'єкт Database для модульних тестів
    :return: Database object
    """
    database = Database(test=True)

    # Знищує стару тестову базу та створює нову
    await database.init_models()
    return database


@pytest_asyncio.fixture
async def client_db(database) -> AsyncClient:  # noqa: F401, F811;
    """
    Створює і повертає httpx.AsyncClient зі створеною тестовою базою
    :return: httpx.AsyncClient
    """
    # перезапис функції, яка буде викликатись у Depends(get_session_depends).
    # За замовчуванням, буде виконуватись метод основої бази.
    # Але тут потрібно використовувати тестову базу, тому залежності перезаписуються
    app.dependency_overrides[
        Database.get_session_depends
    ] = database.get_session_depends
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as session:
        # yield для того, щоб після тесту відбулоась "чистка" фікстури.
        # В цьому випадку це вихід з контекстного менеджера, який закриє клієнт
        yield session
