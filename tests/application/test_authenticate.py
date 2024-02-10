from unittest.mock import Mock

import pytest
from pytest import fixture

from costy.application.authenticate import Authenticate, LoginInputDTO
from costy.application.common.uow import UoW
from costy.application.common.user_gateway import UserReader
from costy.domain.models.user import User, UserId


@fixture
def login_info() -> LoginInputDTO:
    return LoginInputDTO(email="test@email.com", password="password")


@fixture
def interactor(user_id, login_info):
    user_gateway = Mock(spec=UserReader)
    user_gateway.get_user_by_email.return_value = User(
        id=user_id, email=login_info.email,
        hashed_password=login_info.password,
    )
    uow = Mock(spec=UoW)
    return Authenticate(user_gateway, uow)


@pytest.mark.asyncio
async def test_authenticate(interactor: Authenticate, user_id: UserId, login_info: LoginInputDTO):
    assert await interactor(login_info) == user_id
