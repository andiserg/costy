"""
Testing app.main
"""

import pytest
from httpx import AsyncClient

from app.database.database import Database
from app.main import app
from app.main import database as default_database

# Імпорт потрібний для роботи @pytest.mark.anyio
from app.tests.config import anyio_backend, precents_evn_variables


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
@precents_evn_variables
async def test_db_version():
    """
    Тестування app.main.say_db_version
    """
    database = Database(test=True)
    app.dependency_overrides[
        default_database.get_session_depends
    ] = database.get_session_depends
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as client:
        response = await client.get("/database_info/")
        assert response.status_code == 200
        assert "message" in response.json()
