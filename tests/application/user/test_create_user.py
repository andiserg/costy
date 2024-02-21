from unittest.mock import Mock

import pytest
from pytest import fixture

from costy.application.common.uow import UoW
from costy.application.common.user_gateway import UserSaver
from costy.application.user.create_user import CreateUser
from costy.application.user.dto import NewUserDTO
from costy.domain.models.user import User, UserId
from costy.domain.services.user import UserService


@fixture
def user_info() -> NewUserDTO:
    return NewUserDTO(email="test@email.com", password="password")


@fixture
def interactor(user_id: UserId, user_info: NewUserDTO) -> CreateUser:
    user_service = Mock(spec=UserService)
    user_service.create.return_value = User(
        id=None,
    )

    async def mock_save_user(user: User) -> None:
        user.id = user_id

    user_gateway = Mock(spec=UserSaver)
    user_gateway.save_user = mock_save_user
    uow = Mock(spec=UoW)
    return CreateUser(user_service, user_gateway, uow)


@pytest.mark.asyncio
async def test_create_user(interactor: CreateUser, user_info: NewUserDTO, user_id: UserId) -> None:
    assert await interactor(user_info) == user_id
