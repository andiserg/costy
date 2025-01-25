import os

import pytest
from pytest_asyncio import fixture


@fixture(scope="session")
async def db_url() -> str:  # type: ignore
    try:
        return os.environ["TEST_DB_URL"]
    except KeyError:
        pytest.fail("TEST_DB_URL env variable not set")


@fixture(scope="session")
async def auth_sub() -> str:  # type: ignore
    try:
        return os.environ["TEST_AUTH_USER_SUB"].replace("auth0|", "")
    except KeyError:
        pytest.fail("No test user sub environment variable.")


@fixture
async def credentials() -> dict[str, str]:  # type: ignore
    try:
        return {
            "username": os.environ["TEST_AUTH_USER"],
            "password": os.environ["TEST_AUTH_PASSWORD"],
        }
    except KeyError:
        pytest.fail("No test user credentials.")


@fixture
async def monobank_access_data() -> dict[str, str]:
    value = {}
    try:
        value["X-Token"] = os.environ["TEST_MONOBANK_TOKEN"]
    except KeyError:
        pytest.fail("Missing TEST_MONOBANK_TOKEN environment variable")
    return value
