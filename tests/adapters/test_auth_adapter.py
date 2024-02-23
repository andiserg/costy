import os

import pytest
from pytest_asyncio import fixture
from sqlalchemy import Table, insert
from sqlalchemy.ext.asyncio import AsyncSession

from costy.adapters.auth.auth_gateway import AuthGateway
from costy.application.common.auth_gateway import AuthLoger
from costy.domain.models.user import UserId
from costy.infrastructure.config import AuthSettings, get_auth_settings


@fixture
async def auth_sub() -> str:  # type: ignore
    try:
        return os.environ["TEST_AUTH_USER_SUB"]
    except KeyError:
        pytest.skip("No test user sub environment variable.")


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


@fixture
async def created_user(db_session: AsyncSession, db_tables: dict[str, Table], auth_sub: str) -> UserId:
    stmt = insert(db_tables["users"]).values(auth_id=auth_sub)
    result = await db_session.execute(stmt)
    await db_session.flush()
    created_user_id = result.inserted_primary_key[0]
    return UserId(created_user_id)


@pytest.mark.asyncio
async def test_authenticate(auth_adapter: AuthLoger, credentials: dict[str, str]):
    token = await auth_adapter.authenticate(credentials["username"], credentials["password"])
    assert isinstance(token, str)


# @pytest.mark.asyncio
# async def test_get_user_id_by_sup(auth_adapter: AuthLoger, auth_sub: str, created_user: UserId):
#     created_user_id = await auth_adapter.get_user_id_by_auth_id(auth_sub)
#     assert created_user_id == created_user
