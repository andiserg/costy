import pytest

from costy.domain.models.category import Category, CategoryId, CategoryType
from costy.domain.models.operation import Operation
from costy.domain.models.user import UserId
from costy.domain.services.category import CategoryService
from costy.domain.services.operation import OperationService


@pytest.mark.parametrize("domain_service, model, data, expected_model", [
    (
        OperationService(),
        Operation(
            id=None,
            amount=100,
            description="desc",
            time=10000,
            user_id=UserId(9999),
            category_id=CategoryId(9999)
        ),
        (200, "desc_new", 20000, CategoryId(9998)),
        Operation(
            id=None,
            amount=200,
            description="desc_new",
            time=20000,
            user_id=UserId(9999),
            category_id=CategoryId(9998)
        )
    ),
    (
        CategoryService(),
        Category(id=None, name="test", kind=CategoryType.GENERAL.value, user_id=UserId(9999)),
        ("test_new", None),
        Category(id=None, name="test_new", kind=CategoryType.GENERAL.value, user_id=UserId(9999))
    ),
])
@pytest.mark.asyncio
async def test_update_domain_service(domain_service, model, data, expected_model):  # type: ignore
    domain_service.update(model, *data)
    assert model == expected_model
