import json
from importlib import resources
from unittest.mock import Mock

from pytest_asyncio import fixture

from auth.adapters.auth_gateway import AuthAdapter
from auth.adapters.user_gateway import UserAdapter
from auth.config import AuthSettings, get_auth_settings
from costy.adapters.bankapi.bank_gateway import BankAdapter, MCCBankOperation
from costy.adapters.bankapi.bankapi import BankAPIAdapter
from costy.adapters.bankapi.monobank import MonobankAdapter
from costy.adapters.db.category_gateway import CategoryAdapter
from costy.adapters.db.operation_gateway import OperationAdapter
from costy.application.common.id_provider import IdProvider
from costy.domain.models.operation import Operation, OperationId


@fixture(scope="session")
async def auth_settings() -> AuthSettings:
    return get_auth_settings()


@fixture
async def user_gateway(db_session, db_tables) -> UserAdapter:
   return UserAdapter(db_session)


@fixture
async def category_gateway(db_session, db_tables) -> CategoryAdapter:
    return CategoryAdapter(db_session)


@fixture
async def operation_gateway(db_session, db_tables) -> OperationAdapter:
    return OperationAdapter(db_session)

@fixture
async def auth_adapter(db_session, web_session, auth_settings) -> AuthAdapter:
    return AuthAdapter(db_session, web_session, auth_settings)


@fixture
async def id_provider(user_id: int) -> IdProvider:
    provider = Mock(spec=IdProvider)
    provider.get_current_user_id.return_value = user_id
    return provider


@fixture
async def monobank_adapter(web_session) -> MonobankAdapter:
    with open(str(resources.files("costy.adapters.bankapi") / "_banks.json"), "r") as f:
        banks = json.load(f)

    return MonobankAdapter(web_session, banks)


@fixture
async def bankapi_gateway(db_session, web_session, db_tables, retort, user_id, category_gateway):
    bank_adapter = Mock(spec=BankAdapter)
    bank_adapter.fetch_operations.return_value = [
        MCCBankOperation(
            operation=Operation(
                id=OperationId(i),
                amount=100*i,
                description="desc",
                time=1111*i,
                user_id=user_id,
            ),
            mcc=i*1000,
        )
        for i in range(10)
    ]

    gateway_map = {"test_bank": bank_adapter}
    with open(str(resources.files("costy.adapters.bankapi") / "_banks.json"), "r") as f:
        banks_info = json.load(f)

    return BankAPIAdapter(db_session, web_session, gateway_map, banks_info, category_gateway)


@fixture(scope="session")
async def mock_monobank_gateway(bank_operations):
    class MockMonobankGateway:
        def __init__(self, *args, **kwargs):
            pass

        async def fetch_operations(self, *args, **kwargs):
            return bank_operations

    return {"monobank", MockMonobankGateway()}
