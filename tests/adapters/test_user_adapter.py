import pytest

from tests.common.database import create_user


@pytest.mark.asyncio
async def test_get_user_id_by_auth_id(db_session, db_tables, user_gateway, auth_id: str):
    user_id = await create_user(db_session, db_tables["users"], auth_id=auth_id)
    assert await user_gateway.get_user_id_by_auth_id(auth_id) == user_id


@pytest.mark.asyncio
async def test_get_user_by_id(db_session, db_tables, user_gateway, auth_id: str):
    user_id = await create_user(db_session, db_tables["users"], auth_id=auth_id)
    assert (await user_gateway.get_user_by_id(user_id)).id == user_id


@pytest.mark.asyncio
async def test_save_user(user_entity, user_gateway):
    user_entity.auth_id = "unique_auth_id"
    await user_gateway.save_user(user_entity)
    assert user_entity.id is not None
