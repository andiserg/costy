import pytest
from pytest_asyncio import fixture
from sqlalchemy import Table, insert
from sqlalchemy.ext.asyncio import AsyncSession

from costy.application.common.auth_gateway import AuthLoger
from costy.domain.models.user import UserId


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
