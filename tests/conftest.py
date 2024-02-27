import os
from unittest.mock import Mock

import pytest
from pytest_asyncio import fixture

from costy.application.common.id_provider import IdProvider
from costy.domain.models.user import UserId

pytest_plugins = [
    "tests.fixtures.adapters",
    "tests.fixtures.infrastructure",
    "tests.fixtures.db",
    "tests.fixtures.templates",
]


@fixture
async def credentials() -> dict[str, str]:  # type: ignore
    try:
        return {
            "username": os.environ["TEST_AUTH_USER"],
            "password": os.environ["TEST_AUTH_PASSWORD"]
        }
    except KeyError:
        pytest.skip("No test user credentials.")


# global is used because tests cannot use a "session" fixed fixture in this case
user_token_state = None


@fixture
async def user_token(auth_adapter, credentials):  # type: ignore
    global user_token_state
    if not user_token_state:
        response = await auth_adapter.authenticate(credentials["username"], credentials["password"])
        if response:
            return response
        pytest.skip("Failed to test user authenticate.")
    else:
        return user_token_state


@fixture
async def auth_sub() -> str:  # type: ignore
    try:
        return os.environ["TEST_AUTH_USER_SUB"].replace("auth|0", "")
    except KeyError:
        pytest.skip("No test user sub environment variable.")


@fixture
async def id_provider(user_id: UserId) -> IdProvider:
    provider = Mock(spec=IdProvider)
    provider.get_current_user_id.return_value = user_id
    return provider
