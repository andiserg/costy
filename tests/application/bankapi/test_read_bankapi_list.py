from unittest.mock import Mock

import pytest
from pytest_asyncio import fixture

from costy.application.bankapi.read_bankapi_list import ReadBankapiList
from costy.application.common.bankapi.bankapi_gateway import BanksAPIReader
from costy.domain.models.bankapi import BankAPI, BankApiId


@fixture
async def interactor(id_provider, user_id) -> ReadBankapiList:
    bankapi_gateway = Mock(spec=BanksAPIReader)
    bankapi_gateway.get_bankapi_list.return_value = [
        BankAPI(
            id=BankApiId(0),
            user_id=user_id,
            name="bank1",
            access_data={"key1": "value1"},
        ),
        BankAPI(
            id=BankApiId(1),
            user_id=user_id,
            name="bank2",
            access_data={"key2": "value2"},
        ),
    ]

    return ReadBankapiList(bankapi_gateway, id_provider)


@pytest.mark.asyncio()
async def test_get_bankapi_list(interactor):
    assert await interactor()
