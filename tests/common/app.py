import os

import pytest
from adaptix import Retort
from httpx import AsyncClient
from litestar import Litestar
from litestar.di import Provide

from costy.adapters.db.user_gateway import UserGateway
from costy.application.common.id_provider import IdProvider
from costy.domain.exceptions.base import BaseError
from costy.domain.models.user import UserId
from costy.infrastructure.auth import create_id_provider_factory
from costy.infrastructure.config import get_auth_settings, get_banks_conf, get_db_connection_url
from costy.infrastructure.db.main import get_engine, get_metadata, get_sessionmaker
from costy.infrastructure.db.tables import create_tables
from costy.main.ioc import IoC
from costy.main.web import singleton
from costy.presentation.api.dependencies.id_provider import get_id_provider
from costy.presentation.api.exception_handlers import base_error_handler
from costy.presentation.api.routers.authenticate import AuthenticationController
from costy.presentation.api.routers.bankapi import BankAPIController
from costy.presentation.api.routers.category import CategoryController
from costy.presentation.api.routers.operation import OperationController
from costy.presentation.api.routers.user import UserController


class MockIdProvider(IdProvider):
    async def get_current_user_id(self) -> UserId:  # type: ignore
        pass


async def init_test_app(db_url: str | None = None, mock_auth: bool = True, mock_bank_gateways=None):
    if not db_url:
        db_url = get_db_connection_url()

    base_metadata = get_metadata()
    tables = create_tables(base_metadata)

    session_factory = get_sessionmaker(get_engine(db_url))
    web_session = AsyncClient()

    banks_conf = get_banks_conf()

    retort = Retort()
    auth_settings = get_auth_settings()
    ioc = IoC(session_factory, web_session, tables, retort, auth_settings, banks_conf)

    if not mock_bank_gateways:
        ioc._bank_gateways = mock_bank_gateways

    if mock_auth:
        sub = os.environ.get("TEST_AUTH_USER_SUB")
        if not sub:
            pytest.fail("TEST_AUTH_USER_SUB environment not exists")
        else:
            sub = sub.replace("auth0|", "")

        async def get_user_id():
            async with session_factory() as session:
                user_gateway = UserGateway(session, tables["users"], retort)
                return await user_gateway.get_user_id_by_auth_id(sub)

        id_provider: IdProvider = MockIdProvider()
        id_provider.get_current_user_id = get_user_id  # type: ignore
        id_provider_factory = singleton(id_provider)
    else:
        id_provider_factory = create_id_provider_factory(
            auth_settings.audience,
            "RS256",
            auth_settings.issuer,
            auth_settings.jwks_uri,
            web_session,
        )

    return Litestar(
        route_handlers=(
            AuthenticationController,
            UserController,
            OperationController,
            CategoryController,
            BankAPIController,
        ),
        dependencies={
            "ioc": Provide(singleton(ioc)),
            "id_provider": Provide(get_id_provider),
            "id_provider_blank": Provide(id_provider_factory),
        },
        debug=True,
        exception_handlers={
            BaseError: base_error_handler,
        },
    )
