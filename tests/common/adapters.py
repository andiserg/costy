import json
from importlib import resources
from unittest.mock import Mock

from pytest_asyncio import fixture

from costy.adapters.auth.auth_gateway import AuthGateway
from costy.adapters.bankapi.bank_gateway import BankGateway
from costy.adapters.bankapi.bankapi import BankAPIGateway
from costy.adapters.bankapi.monobank import MonobankGateway
from costy.adapters.db.category_gateway import CategoryGateway
from costy.adapters.db.operation_gateway import OperationGateway
from costy.adapters.db.user_gateway import UserGateway
from costy.application.common.auth_gateway import AuthLoger
from costy.application.common.bankapi.dto import BankOperationDTO
from costy.application.common.id_provider import IdProvider
from costy.domain.models.operation import Operation, OperationId
from costy.domain.models.user import UserId
from costy.infrastructure.config import AuthSettings, get_auth_settings


@fixture(scope="session")
async def auth_settings() -> AuthSettings:
    return get_auth_settings()


@fixture
async def auth_adapter(db_session, web_session, db_tables, auth_settings: AuthSettings) -> AuthLoger:
    return AuthGateway(db_session, web_session, db_tables["users"], auth_settings)


@fixture
async def user_gateway(db_session, db_tables, retort) -> UserGateway:
    return UserGateway(db_session, db_tables["users"], retort)


@fixture
async def category_gateway(db_session, db_tables, retort) -> CategoryGateway:
    return CategoryGateway(db_session, db_tables["categories"], db_tables["category_mcc"], retort)


@fixture
async def operation_gateway(db_session, db_tables, retort) -> OperationGateway:
    return OperationGateway(db_session, db_tables["operations"], retort)


@fixture
async def id_provider(user_id: UserId) -> IdProvider:
    provider = Mock(spec=IdProvider)
    provider.get_current_user_id.return_value = user_id
    return provider


@fixture
async def monobank_adapter(web_session, retort) -> MonobankGateway:
    with open(str(resources.files("costy.adapters.bankapi") / "_banks.json"), "r") as f:
        banks = json.load(f)

    return MonobankGateway(web_session, banks, retort)


@fixture
async def bankapi_gateway(db_session, web_session, db_tables, retort, user_id):
    bank_adapter = Mock(spec=BankGateway)
    bank_adapter.fetch_operations.return_value = [
        BankOperationDTO(
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

    return BankAPIGateway(db_session, web_session, db_tables["bankapis"], retort, gateway_map, banks_info)


@fixture(scope="session")
async def mock_monobank_gateway(bank_operations):
    class MockMonobankGateway:
        def __init__(self, *args, **kwargs):
            pass

        async def fetch_operations(self, *args, **kwargs):
            return bank_operations

    return {"monobank", MockMonobankGateway()}
