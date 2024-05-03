from unittest.mock import Mock

import pytest
from pytest_asyncio import fixture

from costy.application.authenticate import Authenticate, LoginInputDTO
from costy.application.common.auth_gateway import AuthLoger
from costy.application.common.uow import UoW
from costy.domain.models.user import UserId


@fixture
async def interactor(user_id: UserId, login_info: LoginInputDTO, token) -> Authenticate:
    auth_gateway = Mock(spec=AuthLoger)
    auth_gateway.authenticate.return_value = token
    uow = Mock(spec=UoW)
    return Authenticate(auth_gateway, uow)


@pytest.mark.asyncio()
async def test_authenticate(interactor: Authenticate, user_id: UserId, login_info: LoginInputDTO, token: str) -> None:
    assert await interactor(login_info) == token
