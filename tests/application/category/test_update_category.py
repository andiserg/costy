from unittest.mock import Mock

import pytest
from pytest_asyncio import fixture

from costy.adapters.db.category_gateway import CategoryGateway
from costy.application.category.update_category import UpdateCategory
from costy.application.common.category.dto import UpdateCategoryData, UpdateCategoryDTO
from costy.application.common.uow import UoW
from costy.domain.exceptions.access import AccessDeniedError
from costy.domain.exceptions.base import InvalidRequestError
from costy.domain.models.category import Category, CategoryId
from costy.domain.models.user import UserId
from costy.domain.services.access import AccessService
from costy.domain.services.category import CategoryService


@fixture
async def interactor(
        user_id: UserId,
        category_id: CategoryId,
        id_provider,
) -> UpdateCategory:
    category_gateway = Mock(spec=CategoryGateway)
    category_gateway.get_category_by_id.return_value = Category(
        id=category_id,
        name="test",
        user_id=user_id,
    )
    uow = Mock(spec=UoW)
    return UpdateCategory(CategoryService(), AccessService(), category_gateway, id_provider, uow)


@pytest.mark.asyncio()
async def test_update_category(interactor: UpdateCategory, category_id: CategoryId):
    update_data = UpdateCategoryDTO(category_id, UpdateCategoryData(name="upd_test"))
    try:
        await interactor(update_data)
    except (AccessDeniedError, InvalidRequestError) as err:
        pytest.fail(f"Update category interactor raise error: {err}")
