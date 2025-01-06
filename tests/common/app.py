from typing import Any

from dishka import AsyncContainer, Provider, Scope, from_context, make_async_container
from dishka.integrations.litestar import setup_dishka
from httpx import AsyncClient
from litestar import Controller, Litestar
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from auth.config import AuthSettings, SettingError, get_auth_settings
from costy.adapters.bankapi.bank_gateway import BankAdapter
from costy.domain.exceptions.base import BaseError
from costy.infrastructure.config import get_banks_conf, get_db_connection_url
from costy.infrastructure.db.main import get_engine, get_sessionmaker
from costy.presentation.api.exception_handlers import base_error_handler


class TestDIProvider(Provider):
    bank_gateways = from_context(dict[str, BankAdapter], scope=Scope.APP)


async def init_test_app(
    db_url: str | None = None,
    mock_bank_gateways: dict[str, BankAdapter] | None = None,
    di_providers: list[Any] | None = None,
    controllers: list[Controller] | None = None,

):
    if not db_url:
        db_url = get_db_connection_url()

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
        dict[str, dict[str, Any]]: get_banks_conf(),
    }

    if not mock_bank_gateways:
        context[dict[str, BankAdapter]] = mock_bank_gateways

    # if mock_auth:
        # sub = os.environ.get("TEST_AUTH_USER_SUB")
        # if not sub:
        #     pytest.fail("TEST_AUTH_USER_SUB environment not exists")
        # else:
        #     sub = sub.replace("auth0|", "")
        #
        # async def get_user_id():
        #     async with session_factory() as session:
        #         user_gateway = UserAdapter(session)
        #         return await user_gateway.get_user_id_by_auth_id(sub)
        #
        # id_provider: IdProvider = MockIdProvider()
        # id_provider.get_current_user_id = get_user_id  # type: ignore
        # context[IdProvider] = id_provider

    container = make_async_container(*di_providers, TestDIProvider(), context=context)

    app = Litestar(
        route_handlers=controllers,
        debug=True,
        exception_handlers={
            BaseError: base_error_handler,
        },
    )
    setup_dishka(container, app)
    return app
