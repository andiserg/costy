"""
Фікстури і інші структури, які використовуються у тестах
"""
import os

import pytest

# Декоратор-перевірка на те, чи існує файл "pytest.ini"
# або існують потрібні ENV параметри
# pytest.ini включений у .gitignore,
# тому такі CI як Github Actions не зможуть корректно
# провести тести і вони пропускаються.
precents_evn_variables = pytest.mark.skipif(
    all(
        [
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


@pytest.fixture
def anyio_backend():
    """
    За замовчуванням, async тест який обернутий в @pytest.mark.anyio
    намагається виконатись також у trio, альтернативі asyncio, і видає failed результат.
    Фікстура вказує, що потрібно перевіряти тільки за допомогою asyncio
    """
    return "asyncio"
