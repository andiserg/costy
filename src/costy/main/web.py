import os
from typing import Any, Callable, Coroutine, TypeVar

from adaptix import Retort
from aiohttp import ClientSession
from litestar import Litestar
from litestar.di import Provide
from sqlalchemy.orm import registry

from costy.infrastructure.auth import create_id_provider_factory
from costy.infrastructure.config import get_db_connection_url
from costy.infrastructure.db.main import get_engine, get_sessionmaker
from costy.infrastructure.db.orm import create_tables, map_tables_to_models
from costy.main.ioc import IoC
from costy.presentation.api.category import CategoryController
from costy.presentation.api.dependencies.id_provider import get_id_provider
from costy.presentation.api.operation import OperationController
from costy.presentation.api.user import UserController

T = TypeVar('T')


def singleton(instance: T) -> Callable[[], Coroutine[Any, Any, T]]:
    async def func() -> T:
        return instance

    return func


def init_app() -> Litestar:
    session_factory = get_sessionmaker(get_engine(get_db_connection_url()))
    ioc = IoC(session_factory=session_factory, retort=Retort())

    web_session = ClientSession()
    id_provider_factory = create_id_provider_factory(
        os.environ.get("AUTH0_AUDIENCE", ""),
        "RS256",
        os.environ.get("AUTH0_ISSUER", ""),
        os.environ.get("AUTH0_JWKS_URI", ""),
        web_session
    )

    mapper_registry = registry()
    tables = create_tables(mapper_registry)
    map_tables_to_models(mapper_registry, tables)

    return Litestar(
        route_handlers=(
            UserController,
            OperationController,
            CategoryController
        ),
        dependencies={
            "ioc": Provide(singleton(ioc)),
            "id_provider": Provide(get_id_provider),
            "id_provider_factory": Provide(id_provider_factory)
        },
        on_shutdown=[lambda: web_session.close()],
        debug=True
    )
