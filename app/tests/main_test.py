"""
Testing app.main
"""

import pytest
from httpx import AsyncClient

from app.database.database import Database
from app.main import app
from app.main import database as default_database

# event_loop, database потрібні для правильного функціонування тестів
from app.tests.config import database, event_loop, precents_evn_variables


@pytest.mark.asyncio
async def test_root():
    """
    Тестування app.main.root
    """
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as client:
        response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.asyncio
@precents_evn_variables
async def test_db_version(database):
    """
    Тестування app.main.say_db_version
    """
    app.dependency_overrides[
        default_database.get_session_depends
    ] = database.get_session_depends
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as client:
        response = await client.get("/database_info/")
        assert response.status_code == 200
        assert "message" in response.json()
