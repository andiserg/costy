from unittest.mock import Mock

from pytest_asyncio import fixture
from sqlalchemy import insert

from costy.application.common.id_provider import IdProvider
from costy.domain.models.category import CategoryId
from costy.domain.models.operation import OperationId
from costy.domain.models.user import UserId

pytest_plugins = ["tests.infrastructure"]


@fixture
def user_id() -> UserId:
    return UserId(999)


@fixture
def operation_id() -> OperationId:
    return OperationId(999)


@fixture
def category_id() -> CategoryId:
    return CategoryId(999)


@fixture()
async def created_user(db_session, db_tables, auth_id) -> UserId:
    result = await db_session.execute(insert(db_tables["users"]).values(auth_id=auth_id))
    return UserId(result.inserted_primary_key[0])


@fixture
def id_provider(user_id: UserId) -> IdProvider:
    provider = Mock(spec=IdProvider)
    provider.get_current_user_id.return_value = user_id
    return provider
