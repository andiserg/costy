import os
from typing import Any

import pytest
from adaptix import Retort
from dishka import make_async_container, Scope, Provider, from_context
from dishka.integrations.litestar import setup_dishka
from httpx import AsyncClient
from litestar import Litestar
from sqlalchemy import Table
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from costy.adapters.bankapi.bank_gateway import BankGateway
from costy.adapters.db.user_gateway import UserGateway
from costy.application.common.id_provider import IdProvider
from costy.domain.exceptions.base import BaseError
from costy.domain.models.user import UserId
from costy.infrastructure.config import get_auth_settings, get_banks_conf, get_db_connection_url, AuthSettings
from costy.infrastructure.db.main import get_engine, get_metadata, get_sessionmaker
from costy.infrastructure.db.tables import create_tables
from costy.main.di import DIProvider
from costy.presentation.api.exception_handlers import base_error_handler
from costy.presentation.api.routers.authenticate import AuthenticationController
from costy.presentation.api.routers.bankapi import BankAPIController
from costy.presentation.api.routers.category import CategoryController
from costy.presentation.api.routers.operation import OperationController
from costy.presentation.api.routers.user import UserController


class MockIdProvider(IdProvider):
    async def get_current_user_id(self) -> UserId:  # type: ignore
        pass


class TestIdDIProvider(Provider):
    id_provider = from_context(IdProvider, scope=Scope.APP)
    bank_gateways = from_context(dict[str, BankGateway], scope=Scope.APP)


async def init_test_app(
    db_url: str | None = None,
    mock_auth: bool = True,
    mock_bank_gateways: dict[str, BankGateway] | None = None
):
    if not db_url:
        db_url = get_db_connection_url()

    base_metadata = get_metadata()
    tables = create_tables(base_metadata)

    session_factory = get_sessionmaker(get_engine(db_url))
    web_session = AsyncClient()

    retort = Retort()
    auth_settings = get_auth_settings()

    context = {
        AsyncClient: web_session,
        async_sessionmaker[AsyncSession]: session_factory,
        dict[str, Table]: tables,
        AuthSettings: auth_settings,
        dict[str, Any]: get_banks_conf(),
        Retort: retort
    }

    if not mock_bank_gateways:
        context[dict[str, BankGateway]] = mock_bank_gateways

    if mock_auth:
        sub = os.environ.get("TEST_AUTH_USER_SUB")
        if not sub:
            pytest.fail("TEST_AUTH_USER_SUB environment not exists")
        else:
            sub = sub.replace("auth0|", "")

        async def get_user_id():
            async with session_factory() as session:
                user_gateway = UserGateway(session, tables["users"])
                return await user_gateway.get_user_id_by_auth_id(sub)

        id_provider: IdProvider = MockIdProvider()
        id_provider.get_current_user_id = get_user_id  # type: ignore
        context[IdProvider] = id_provider

    container = make_async_container(DIProvider(), TestIdDIProvider(), context=context)

    app = Litestar(
        route_handlers=(
            AuthenticationController,
            UserController,
            OperationController,
            CategoryController,
            BankAPIController,
        ),
        debug=True,
        exception_handlers={
            BaseError: base_error_handler,
        },
    )
    setup_dishka(container, app)
    return app
