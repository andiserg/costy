from typing import Any, Callable, Coroutine, TypeVar

from adaptix import Retort
from httpx import AsyncClient
from litestar import Litestar
from litestar.di import Provide

from costy.infrastructure.auth import create_id_provider_factory
from costy.infrastructure.config import (
    get_auth_settings,
    get_db_connection_url,
)
from costy.infrastructure.db.main import (
    get_engine,
    get_metadata,
    get_sessionmaker,
)
from costy.infrastructure.db.orm import create_tables
from costy.main.ioc import IoC
from costy.presentation.api.authenticate import AuthenticationController
from costy.presentation.api.category import CategoryController
from costy.presentation.api.dependencies.id_provider import get_id_provider
from costy.presentation.api.operation import OperationController
from costy.presentation.api.user import UserController

T = TypeVar('T')


def singleton(instance: T) -> Callable[[], Coroutine[Any, Any, T]]:
    async def func() -> T:
        return instance

    return func


def init_app(db_url: str | None = None) -> Litestar:
    if not db_url:
        db_url = get_db_connection_url()

    base_metadata = get_metadata()
    tables = create_tables(base_metadata)

    session_factory = get_sessionmaker(get_engine(db_url))
    web_session = AsyncClient()

    auth_settings = get_auth_settings()
    ioc = IoC(session_factory, web_session, tables, Retort(), auth_settings)

    id_provider_factory = create_id_provider_factory(
        auth_settings.audience,
        "RS256",
        auth_settings.issuer,
        auth_settings.jwks_uri,
        web_session
    )

    async def finalization():
        await web_session.aclose()

    return Litestar(
        route_handlers=(
            AuthenticationController,
            UserController,
            OperationController,
            CategoryController,
        ),
        dependencies={
            "ioc": Provide(singleton(ioc)),
            "id_provider": Provide(get_id_provider),
            "id_provider_pure": Provide(id_provider_factory)
        },
        on_shutdown=[finalization],
        debug=True
    )
