import os

import pytest
from pytest_asyncio import fixture

from costy.application.common.bankapi.dto import BankOperationDTO


@fixture
async def monobank_access_data() -> dict[str, str]:
    try:
        token = os.environ["TEST_MONOBANK_TOKEN"]
    except KeyError:
        pytest.fail("Missing TEST_MONOBANK_TOKEN environment variable")

    return {"X-Token": token}


@pytest.mark.asyncio()
async def test_fetch_operations(monobank_adapter, monobank_access_data, user_id):
    result = await monobank_adapter.fetch_operations(monobank_access_data, user_id)

    assert isinstance(result, list)

    if len(result) > 0:
        assert all(isinstance(dto, BankOperationDTO) for dto in result)
