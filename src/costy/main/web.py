from typing import Any, Callable, Coroutine, TypeVar

from adaptix import Retort
from httpx import AsyncClient
from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.di import Provide

from costy.domain.exceptions.base import BaseError
from costy.infrastructure.auth import create_id_provider_factory
from costy.infrastructure.config import get_auth_settings, get_banks_conf, get_db_connection_url, setup_logger
from costy.infrastructure.db.main import get_engine, get_metadata, get_sessionmaker
from costy.infrastructure.db.tables import create_tables
from costy.main.ioc import IoC
from costy.presentation.api.dependencies.id_provider import get_id_provider
from costy.presentation.api.exception_handlers import base_error_handler
from costy.presentation.api.routers.authenticate import AuthenticationController
from costy.presentation.api.routers.bankapi import BankAPIController
from costy.presentation.api.routers.category import CategoryController
from costy.presentation.api.routers.operation import OperationController
from costy.presentation.api.routers.user import UserController

T = TypeVar("T")


def singleton(instance: T) -> Callable[[], Coroutine[Any, Any, T]]:
    async def func() -> T:
        return instance

    return func


def init_app() -> Litestar:
    setup_logger()

    base_metadata = get_metadata()
    web_session = AsyncClient()
    auth_settings = get_auth_settings()

    ioc = IoC(
        get_sessionmaker(get_engine(get_db_connection_url())),
        web_session,
        create_tables(base_metadata),
        Retort(),
        auth_settings,
        get_banks_conf(),
    )

    id_provider_factory = create_id_provider_factory(
        auth_settings.audience,
        "RS256",
        auth_settings.issuer,
        auth_settings.jwks_uri,
        web_session,
    )

    async def finalization():
        await web_session.aclose()

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
        on_shutdown=[finalization],
        exception_handlers={
            BaseError: base_error_handler,
        },
        debug=True,
        cors_config=CORSConfig(allow_origins=["*"]),
    )
