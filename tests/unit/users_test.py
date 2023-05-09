import pytest

from src.app.domain.users import User
from src.app.services.users import create_user, get_user_by_email
from src.schemas.users import UserCreateSchema
from tests.fake_adapters.uow import FakeUnitOfWork


@pytest.mark.asyncio
async def test_create_user():
    uow = FakeUnitOfWork()
    schema = UserCreateSchema(email="test", password="test")
    user = await create_user(uow, schema)
    assert user


@pytest.mark.asyncio
async def test_read_user():
    uow = FakeUnitOfWork()
    async with uow:
        uow.users.instances = [User(email="test", hashed_password="test")]
        user = await get_user_by_email(uow, "test")
        assert user
