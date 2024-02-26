import pytest
from pytest_asyncio import fixture

from costy.adapters.db.user_gateway import UserGateway
from costy.domain.models.user import User


@fixture
async def auth_id() -> str:
    return "auth_id"


@fixture
async def user_gateway(db_session, db_tables, retort) -> UserGateway:
    return UserGateway(db_session, db_tables["users"], retort)


@fixture
async def user_entity() -> User:
    return User(id=None, auth_id="auth_id")


@pytest.mark.asyncio
async def test_get_user_id_by_auth_id(created_user, user_gateway, auth_id: str) -> None:
    assert await user_gateway.get_user_id_by_auth_id(auth_id) == created_user


@pytest.mark.asyncio
async def test_get_user_by_id(created_user, user_gateway):
    assert (await user_gateway.get_user_by_id(created_user)).id == created_user


@pytest.mark.asyncio
async def test_save_user(user_entity, user_gateway):
    await user_gateway.save_user(user_entity)
    assert user_entity.id is not None
