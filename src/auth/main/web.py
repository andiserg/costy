from dishka import make_async_container
from dishka.integrations.litestar import setup_dishka
from httpx import AsyncClient
from litestar import Litestar
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from auth.config import AuthSettings, get_auth_settings, get_db_connection_url
from auth.exceptions import BaseError
from auth.handlers import AuthenticationController, UserController, base_error_handler
from auth.infra import get_engine, get_sessionmaker
from auth.main.di import DIProvider


def init_app() -> Litestar:
    web_session = AsyncClient()

    container = make_async_container(
        DIProvider(),
        context={
            AuthSettings: get_auth_settings(),
            AsyncClient: web_session,
            async_sessionmaker[AsyncSession]: get_sessionmaker(
                get_engine(get_db_connection_url()),
            ),
        },
    )

    async def finalization() -> None:
        await web_session.aclose()

    app = Litestar(
        route_handlers=(
            AuthenticationController,
            UserController,
        ),
        on_shutdown=[finalization],
        exception_handlers={BaseError: base_error_handler},
        debug=True,
    )
    setup_dishka(container, app)
    return app
