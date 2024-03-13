import pytest

from costy.domain.models.bankapi import BankAPI
from costy.domain.models.category import Category, CategoryId, CategoryType
from costy.domain.models.operation import Operation
from costy.domain.models.user import User, UserId
from costy.domain.services.bankapi import BankAPIService
from costy.domain.services.category import CategoryService
from costy.domain.services.operation import OperationService
from costy.domain.services.user import UserService


@pytest.mark.parametrize("domain_service, data, expected_model", [
    (
        UserService(),
        ("auth_id",),
        User(id=None, auth_id="auth_id")
    ),
    (
        OperationService(),
        (100, "desc", 10000, UserId(9999), CategoryId(9999)),
        Operation(
            id=None,
            amount=100,
            description="desc",
            time=10000,
            user_id=UserId(9999),
            category_id=CategoryId(9999),
            bank_name=None
        )
    ),
    (
        CategoryService(),
        ("test", CategoryType.GENERAL, UserId(9999)),
        Category(id=None, name="test", kind=CategoryType.GENERAL.value, user_id=UserId(9999), mcc=None)
    ),
    (
        BankAPIService(),
        ("test", {"key": "test"}, UserId(9999)),
        BankAPI(name="test", access_data={"key": "test"}, updated_at=None, user_id=UserId(9999))
    )
])
@pytest.mark.asyncio
async def test_create_domain_service(domain_service, data, expected_model):  # type: ignore
    assert domain_service.create(*data) == expected_model
