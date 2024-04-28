from unittest.mock import Mock

import pytest
from pytest_asyncio import fixture

from costy.application.bankapi.create_bankapi import CreateBankAPI
from costy.application.common.bankapi.dto import CreateBankApiDTO
from costy.application.common.id_provider import IdProvider
from costy.application.common.uow import UoW
from costy.domain.exceptions.base import InvalidRequestError
from costy.domain.models.bankapi import BankAPI
from costy.domain.services.bankapi import BankAPIService


@fixture
async def interactor(id_provider: IdProvider, bankapi_id) -> CreateBankAPI:
    async def save_bankapi_mock(bankapi: BankAPI) -> None:
        bankapi.id = bankapi_id

    async def get_supported_banks():
        return ["test_bank"]

    async def access_data_template(*args, **kwargs):
        return ("key",)

    bankapi_gateway = Mock()
    bankapi_gateway.save_bankapi = save_bankapi_mock
    bankapi_gateway.get_supported_banks = get_supported_banks
    bankapi_gateway.get_bank_access_data_template = access_data_template

    uow = Mock(spec=UoW)
    return CreateBankAPI(BankAPIService(), bankapi_gateway, id_provider, uow)


@pytest.mark.asyncio()
async def test_create_bankapi(interactor: CreateBankAPI):
    data = CreateBankApiDTO(name="test_bank", access_data={"key": "value"})
    try:
        await interactor(data)
    except InvalidRequestError:
        pytest.fail("Interactor raises InvalidRequestError")


@pytest.mark.asyncio()
async def test_create_bankapi_with_invalid_bank(interactor: CreateBankAPI):
    data = CreateBankApiDTO(name="invalid_bank", access_data={"key": "value"})

    with pytest.raises(InvalidRequestError) as error:
        await interactor(data)

    assert error.value.args[0] == "This bank is not supported."


@pytest.mark.asyncio()
async def test_create_bankapi_with_invalid_access_data(interactor: CreateBankAPI):
    data = CreateBankApiDTO(name="test_bank", access_data={"invalid_key": "value"})

    with pytest.raises(InvalidRequestError) as error:
        await interactor(data)

    assert error.value.args[0] == "Invalid bank access data."
