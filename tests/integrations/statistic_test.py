import pytest
from httpx import AsyncClient

from tests.patterns import create_and_auth_func_user, create_operations


@pytest.mark.asyncio
async def test_get_statistic(client_db: AsyncClient):
    auth_data = await create_and_auth_func_user(client_db)
    token = auth_data["token"]
    headers = {"Authorization": token}
    await create_operations(headers, client_db)
    response = await client_db.get("/statistic/", headers=headers)
    assert response.status_code == 200
