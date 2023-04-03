"""
Functional users tests
"""

import pytest
from httpx import AsyncClient

# event_loop, database потрібні для правильного функціонування тестів
from tests.config import (  # noqa: F401;
    client_db,
    database,
    event_loop,
    precents_evn_variables,
)
from tests.patterns import create_and_auth_func_user


@pytest.mark.asyncio
async def test_create_user_endpoint(client_db: AsyncClient):  # noqa: F811;
    """
    Testing src.views.users.create_user_view
    """
    data = {"email": "test@mail.test", "password": "123456"}  # nosec B106
    result = await client_db.post("/users/create/", json=data)
    assert result.status_code == 201
    assert all(key in result.json() for key in ["id", "email"])


@pytest.mark.asyncio
async def test_read_user(client_db: AsyncClient):  # noqa: F811;
    """
    Testing src.views.users.read_me
    """
    auth_result = await create_and_auth_func_user(client_db)
    created_user, token = auth_result["user"], auth_result["token"]

    read_result = await client_db.get("/users/me/", headers={"Authorization": token})
    assert read_result.status_code == 200

    user_data = read_result.json()
    assert user_data["email"] == created_user["email"]
