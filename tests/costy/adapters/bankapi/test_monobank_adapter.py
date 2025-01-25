import pytest

from costy.adapters.bankapi.bank_gateway import MCCBankOperation


@pytest.mark.skip()
@pytest.mark.asyncio()
async def test_fetch_operations(monobank_adapter, monobank_access_data, user_id):
    result = await monobank_adapter.fetch_operations(monobank_access_data, user_id)

    assert isinstance(result, list)

    if len(result) > 0:
        assert all(isinstance(dto, MCCBankOperation) for dto in result)
