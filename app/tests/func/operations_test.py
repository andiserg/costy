import random

import pytest
from httpx import AsyncClient

from app.tests.config import (  # noqa: F401;
    client_db,
    database,
    event_loop,
    precents_evn_variables,
)
from app.tests.patterns import create_and_auth_func_user


@pytest.mark.asyncio
async def test_create_operation_endpoint(client_db: AsyncClient):  # noqa: F811;
    """
    Testing app.views.operations.create_operation_view
    """
    auth_data = await create_and_auth_func_user(client_db)
    token = auth_data["token"]

    headers = {"Authorization": token}

    operation_data = {
        "amount": random.randint(-10000, -10),
        "description": "description",
        "mcc": random.randint(1000, 9999),
        "source_type": "manual",
    }
    response = await client_db.post(
        "/operations/create/", json=operation_data, headers=headers
    )
    assert response.status_code == 201

    created_operation = response.json()
    for key, value in operation_data.items():
        assert created_operation[key] == value