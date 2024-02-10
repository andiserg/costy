from unittest.mock import Mock

from pytest import fixture

from costy.application.common.id_provider import IdProvider
from costy.domain.models.category import CategoryId
from costy.domain.models.operation import OperationId
from costy.domain.models.user import UserId


@fixture
def user_id() -> UserId:
    return UserId(999)


@fixture
def operation_id() -> OperationId:
    return OperationId(999)


@fixture
def category_id() -> CategoryId:
    return CategoryId(999)


@fixture
def id_provider(user_id: UserId) -> IdProvider:
    provider = Mock(spec=IdProvider)
    provider.get_current_user_id.return_value = user_id
    return provider
