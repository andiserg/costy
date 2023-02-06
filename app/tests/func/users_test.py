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
    assert result.status_code == 200
    assert all(key in result.json() for key in ["id", "email"])
