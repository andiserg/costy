import os

import pytest
from pytest_asyncio import fixture

from costy.adapters.auth.auth_gateway import AuthGateway
from costy.application.common.auth_gateway import AuthLoger
from costy.infrastructure.config import AuthSettings, get_auth_settings


@fixture
async def auth_settings() -> AuthSettings:
    return get_auth_settings()


@fixture
async def auth_adapter(db_session, web_session, db_tables, auth_settings: AuthSettings) -> AuthLoger:
    return AuthGateway(db_session, web_session, db_tables["users"], auth_settings)


@fixture
async def credentials() -> dict[str, str]:  # type: ignore
    try:
        return {
            "username": os.environ["TEST_AUTH_USER"],
            "password": os.environ["TEST_AUTH_PASSWORD"]
        }
    except KeyError:
        pytest.skip("No test user credentials.")


@pytest.mark.asyncio
async def test_auth_adapter(auth_adapter: AuthLoger, credentials: dict[str, str]):
    result = await auth_adapter.authenticate(credentials["username"], credentials["password"])
    assert isinstance(result, str)
