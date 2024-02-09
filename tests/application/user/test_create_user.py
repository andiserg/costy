from unittest.mock import Mock

import pytest
from pytest import fixture

from costy.application.common.uow import UoW
from costy.application.common.user_gateway import UserSaver
from costy.application.user.create_user import CreateUser, NewUserDTO
from costy.domain.models.user import User, UserId
from costy.domain.services.user import UserService


@fixture
def user_info() -> NewUserDTO:
    return NewUserDTO(email="test@email.com", password="password")


@fixture
def interactor(user_id, user_info):
    user_service = Mock(spec=UserService)
    user_service.create.return_value = User(
        id=None,
        email=user_info.email,
        hashed_password=user_info.password
    )

    async def mock_save_user(user: User):
        user.id = user_id

    user_gateway = Mock(spec=UserSaver)
    user_gateway.save_user = mock_save_user
    uow = Mock(spec=UoW)
    return CreateUser(user_service, user_gateway, uow)


@pytest.mark.asyncio
async def test_create_user(interactor: CreateUser, user_info: NewUserDTO, user_id: UserId):
    assert await interactor(user_info) == user_id
