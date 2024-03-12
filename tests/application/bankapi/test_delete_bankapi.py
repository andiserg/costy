from unittest.mock import Mock

import pytest
from pytest_asyncio import fixture

from costy.application.bankapi.delete_bankapi import DeleteBankAPI
from costy.application.common.id_provider import IdProvider
from costy.application.common.uow import UoW
from costy.domain.exceptions.access import AccessDeniedError
from costy.domain.exceptions.base import InvalidRequestError
from costy.domain.models.bankapi import BankAPI, BankApiId
from costy.domain.services.access import AccessService


@fixture
async def interactor(id_provider: IdProvider, bankapi_id, user_id) -> DeleteBankAPI:
    async def get_bankapi(_id, *args, **kwargs):
        if _id == bankapi_id:
            return BankAPI(id=bankapi_id, name="test_bank", access_data={"key": "value"}, user_id=user_id)

    async def delete_bankapi(*args, **kwargs):
        pass

    bankapi_gateway = Mock()
    bankapi_gateway.get_bankapi = get_bankapi
    bankapi_gateway.delete_bankapi = delete_bankapi

    uow = Mock(spec=UoW)
    return DeleteBankAPI(AccessService(), bankapi_gateway, id_provider, uow)


@pytest.mark.asyncio
async def test_delete_bankapi(interactor: DeleteBankAPI, bankapi_id):
    try:
        await interactor(bankapi_id)
    except InvalidRequestError:
        pytest.fail("Interactor raises InvalidRequestError")


@pytest.mark.asyncio
async def test_delete_bankapi_with_invalid_id(interactor: DeleteBankAPI):
    with pytest.raises(InvalidRequestError) as error:
        await interactor(BankApiId(10000))

    assert error.value.args[0] == "Invalid bankapi id."


@pytest.mark.asyncio
async def test_delete_bankapi_without_permissions(interactor: DeleteBankAPI, bankapi_id):
    interactor._id_provider.get_current_user_id.return_value = -1  # type: ignore

    with pytest.raises(AccessDeniedError) as error:
        await interactor(bankapi_id)

    assert error.value.args[0] == "User does not have permission to delete this bankapi."
