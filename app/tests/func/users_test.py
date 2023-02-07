"""
Functional users tests
"""

import pytest
from httpx import AsyncClient

# event_loop, database потрібні для правильного функціонування тестів
from app.tests.config import (  # noqa: F401;
    client_db,
    database,
    event_loop,
    precents_evn_variables,
)


@pytest.mark.asyncio
async def test_create_user_endpoint(client_db: AsyncClient):  # noqa: F811;
    """
    Testing app.views.users.create_user_view
    """
    data = {"email": "test@mail.test", "password": "123456"}  # nosec B106
    result = await client_db.post("/users/create/", json=data)
    assert result.status_code == 201
    assert all(key in result.json() for key in ["id", "email"])


@pytest.mark.asyncio
async def test_read_user(client_db: AsyncClient):  # noqa: F811;
    """
    Testing app.views.users.read_me
    """
    data = {"email": "test", "username": "test", "password": "test"}  # nosec B106
    await client_db.post("/users/create/", json=data)

    auth_result = await client_db.post("/token/", data=data)
    token = f"Bearer {auth_result.json()['access_token']}"

    read_result = await client_db.get("/users/me/", headers={"Authorization": token})
    assert read_result.status_code == 200

    user_data = read_result.json()
    assert user_data["email"] == data["email"]
