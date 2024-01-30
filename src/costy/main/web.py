from typing import Callable, TypeVar

from litestar import Litestar
from litestar.di import Provide

from costy.infrastructure.config import get_db_connection_url
from costy.infrastructure.db.main import get_engine, get_sessionmaker
from costy.main.ioc import IoC
from costy.presentation.api.dependencies.id_provider import get_id_provider
from costy.presentation.api.user import UserController


T = TypeVar('T')


def singleton(instance: T) -> Callable[[], T]:
    async def func():
        return instance

    return func


def init_app() -> Litestar:
    session_factory = get_sessionmaker(get_engine(get_db_connection_url()))
    ioc = IoC(session_factory=session_factory)

    return Litestar(
        route_handlers=(UserController,),
        dependencies={"ioc": Provide(singleton(ioc)), "id_provider": Provide(get_id_provider)}
    )
