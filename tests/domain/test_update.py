import pytest

from costy.domain.models.category import Category, CategoryId, CategoryType
from costy.domain.models.operation import Operation
from costy.domain.models.user import UserId
from costy.domain.services.category import CategoryService
from costy.domain.services.operation import OperationService


@pytest.mark.parametrize("domain_service, model, data, expected_model", [
    (
        OperationService(),
        Operation(None, 100, "desc", 10000, UserId(9999), CategoryId(9999)),
        (200, "desc_new", 20000, CategoryId(9998)),
        Operation(None, 200, "desc_new", 20000, UserId(9999), CategoryId(9998))
    ),
    (
        CategoryService(),
        Category(None, "test", CategoryType.GENERAL.value, UserId(9999)),
        ("test_new",),
        Category(None, "test_new", CategoryType.GENERAL.value, UserId(9999))
    ),
])
@pytest.mark.asyncio
async def test_create_domain_service(domain_service, model, data, expected_model):  # type: ignore
    domain_service.update(model, *data)
    assert model == expected_model
