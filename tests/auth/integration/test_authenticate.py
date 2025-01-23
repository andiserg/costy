import pytest
from litestar.testing import AsyncTestClient


@pytest.mark.asyncio()
async def test_authenticate(auth_app, credentials):
    async with AsyncTestClient(app=auth_app) as client:
        credentials['email'] = credentials['username']
        credentials.pop('username')

        response = await client.post("/auth", json=credentials)

        assert response.status_code == 200
        assert response.json().get("token")
