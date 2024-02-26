import os

import pytest
from litestar.testing import AsyncTestClient
from pytest_asyncio import fixture


@fixture
async def credentials() -> dict[str, str]:  # type: ignore
    try:
        return {
            "email": os.environ["TEST_AUTH_USER"],
            "password": os.environ["TEST_AUTH_PASSWORD"]
        }
    except KeyError:
        pytest.skip("No test user credentials.")


@pytest.mark.asyncio
@pytest.mark.skip  # TODO: Make up way to run integration tests with aiohttp
async def test_authenticate(app, credentials):
    async with AsyncTestClient(app=app) as client:
        response = await client.post("/auth", json=credentials)
        print("\n\n", response.json(), "\n\n")
        assert response.status_code == 200
        assert response.json().get("token")
