import pytest

from costy.domain.models.category import Category, CategoryId, CategoryType
from costy.domain.models.operation import Operation
from costy.domain.models.user import User, UserId
from costy.domain.services.category import CategoryService
from costy.domain.services.operation import OperationService
from costy.domain.services.user import UserService


@pytest.mark.parametrize("domain_service, data, expected_model", [
    (
        UserService(),
        ("auth_id",),
        User(None, "auth_id")
    ),
    (
        OperationService(),
        (100, "desc", 10000, UserId(9999), CategoryId(9999)),
        Operation(None, 100, "desc", 10000, UserId(9999), CategoryId(9999))
    ),
    (
        CategoryService(),
        ("test", CategoryType.GENERAL, UserId(9999)),
        Category(None, "test", CategoryType.GENERAL.value, UserId(9999))
    ),
])
@pytest.mark.asyncio
async def test_create_domain_service(domain_service, data, expected_model):  # type: ignore
    assert domain_service.create(*data) == expected_model
