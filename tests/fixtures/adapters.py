from pytest_asyncio import fixture

from costy.adapters.auth.auth_gateway import AuthGateway
from costy.adapters.db.category_gateway import CategoryGateway
from costy.adapters.db.operation_gateway import OperationGateway
from costy.adapters.db.user_gateway import UserGateway
from costy.application.common.auth_gateway import AuthLoger
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
    return CategoryGateway(db_session, db_tables["categories"], retort)


@fixture
async def operation_gateway(db_session, db_tables, retort) -> OperationGateway:
    return OperationGateway(db_session, db_tables["operations"], retort)
