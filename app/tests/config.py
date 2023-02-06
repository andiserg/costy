"""
Фікстури і інші структури, які використовуються у тестах
"""
import asyncio
import os

import pytest
import pytest_asyncio

from app.database.database import Database


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
