import pytest


@pytest.mark.asyncio
async def test_get_user_id_by_auth_id(created_auth_user, user_gateway, auth_id: str) -> None:
    assert await user_gateway.get_user_id_by_auth_id(auth_id) == created_auth_user


@pytest.mark.asyncio
async def test_get_user_by_id(created_auth_user, user_gateway):
    assert (await user_gateway.get_user_by_id(created_auth_user)).id == created_auth_user


@pytest.mark.asyncio
async def test_save_user(user_entity, user_gateway):
    await user_gateway.save_user(user_entity)
    assert user_entity.id is not None
