"""
Testing app.main
"""

import pytest
from httpx import AsyncClient

from app.main import app

# Імпорт потрібний для роботи @pytest.mark.anyio
from app.tests.config import anyio_backend


@pytest.mark.anyio
async def test_root():
    """
    Тестування app.main.root
    """
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as client:
        response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.anyio
async def test_db_version():
    """
    Тестування app.main.say_db_version
    """
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as client:
        response = await client.get("/database_info/")
        assert response.status_code == 200
        assert "message" in response.json()
