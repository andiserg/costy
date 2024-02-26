from unittest.mock import Mock

import pytest
from pytest_asyncio import fixture

from costy.application.common.auth_gateway import AuthRegister
from costy.application.common.uow import UoW
from costy.application.common.user_gateway import UserSaver
from costy.application.user.create_user import CreateUser
from costy.application.user.dto import NewUserDTO
from costy.domain.models.user import User, UserId
from costy.domain.services.user import UserService


@fixture
async def user_info() -> NewUserDTO:
    return NewUserDTO(email="test@email.com", password="password")


@fixture
async def interactor(user_id: UserId, user_info: NewUserDTO) -> CreateUser:
    user_service = Mock(spec=UserService)
    user_service.create.return_value = User(id=None, auth_id="auth_id")

    async def mock_save_user(user: User) -> None:
        user.id = user_id

    user_gateway = Mock(spec=UserSaver)
    user_gateway.save_user = mock_save_user
    auth_gateway = Mock(spec=AuthRegister)
    auth_gateway.register.return_value = "auth_id"
    uow = Mock(spec=UoW)
    return CreateUser(user_service, user_gateway, auth_gateway, uow)


@pytest.mark.asyncio
async def test_create_user(interactor: CreateUser, user_info: NewUserDTO, user_id: UserId) -> None:
    assert await interactor(user_info) == user_id
