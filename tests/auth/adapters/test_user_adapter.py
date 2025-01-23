import pytest

from auth.models import User
from tests.common.crud import create_user


@pytest.mark.asyncio()
async def test_get_user_id_by_auth_id(db_session, user_gateway, auth_id: str):
    user_id = await create_user(db_session, auth_id=auth_id)
    assert (await user_gateway.get_user_by_auth_id(auth_id)).id == user_id


@pytest.mark.asyncio()
async def test_get_user_by_id(db_session, user_gateway, auth_id: str):
    user_id = await create_user(db_session, auth_id=auth_id)
    assert (await user_gateway.get_user_by_id(user_id)).id == user_id


@pytest.mark.asyncio()
async def test_save_user(user_gateway):
    user_entity = User(auth_id="unique_auth_id")
    await user_gateway.save_user(user_entity)
    assert user_entity.id is not None
