from typing import Any

from dishka import Provider, Scope, from_context, make_async_container
from dishka.integrations.litestar import setup_dishka
from httpx import AsyncClient
from litestar import Litestar
from pytest_asyncio import fixture
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from auth.config import AuthSettings, SettingError, get_auth_settings
from auth.handlers import AuthenticationController, UserController
from auth.handlers import base_error_handler as auth_error_handler
from auth.main.di import DIProvider as AuthDIProvider
from costy.adapters.bankapi.bank_gateway import BankAdapter
from costy.domain.exceptions.base import BaseError
from costy.infrastructure.config import get_banks_conf
from costy.infrastructure.db.main import get_engine, get_sessionmaker
from costy.main.di import DIProvider as CostyDIProvider
from costy.main.di import IdDIProvider
from costy.presentation.api.exception_handlers import (
    base_error_handler as costy_error_handler,
)
from costy.presentation.api.routers.bankapi import BankAPIController
from costy.presentation.api.routers.category import CategoryController
from costy.presentation.api.routers.operation import OperationController


class TestDIProvider(Provider):
    bank_gateways = from_context(dict[str, BankAdapter], scope=Scope.APP)


@fixture(scope="session")
async def costy_app(db_url, mock_monobank_gateway) -> Litestar:
    session_factory = get_sessionmaker(get_engine(db_url))
    web_session = AsyncClient()

    context = {
        AsyncClient: web_session,
        async_sessionmaker[AsyncSession]: session_factory,
        dict[str, dict[str, Any]]: get_banks_conf(),
        dict[str, BankAdapter]: mock_monobank_gateway
    }

    container = make_async_container(
        IdDIProvider(), CostyDIProvider(), TestDIProvider(), context=context
    )

    app = Litestar(
        route_handlers=[
            BankAPIController,
            CategoryController,
            OperationController
        ],
        debug=True,
        exception_handlers={
            BaseError: costy_error_handler,
        },
    )
    setup_dishka(container, app)
    return app



@fixture(scope="session")
async def auth_app(db_url):
    session_factory = get_sessionmaker(get_engine(db_url))
    web_session = AsyncClient()

    try:
        a_settings = get_auth_settings()
    except SettingError:
        a_settings = None


    context = {
        AuthSettings: a_settings,
        AsyncClient: web_session,
        async_sessionmaker[AsyncSession]: session_factory,
    }

    container = make_async_container(AuthDIProvider(), context=context)

    app = Litestar(
        route_handlers=(
            AuthenticationController,
            UserController,
        ),
        exception_handlers={BaseError: auth_error_handler},
        debug=True,
    )
    setup_dishka(container, app)
    return app
