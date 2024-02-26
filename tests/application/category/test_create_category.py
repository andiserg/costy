from unittest.mock import Mock

import pytest
from pytest_asyncio import fixture

from costy.application.category.create_category import CreateCategory
from costy.application.category.dto import NewCategoryDTO
from costy.application.common.category_gateway import CategorySaver
from costy.application.common.id_provider import IdProvider
from costy.application.common.uow import UoW
from costy.domain.models.category import Category, CategoryId, CategoryType
from costy.domain.models.user import UserId


@fixture
async def category_info() -> NewCategoryDTO:
    return NewCategoryDTO("test")


@fixture
async def interactor(id_provider: IdProvider, category_id: CategoryId, user_id: UserId, category_info: NewCategoryDTO) -> CreateCategory:
    category_service = Mock()
    category_service.create.return_value = Category(
        id=None,
        name=category_info.name,
        kind=CategoryType.PERSONAL.value,
        user_id=user_id,
    )

    async def save_category_mock(category: Category) -> None:
        category.id = category_id

    category_gateway = Mock(spec=CategorySaver)
    category_gateway.save_category = save_category_mock
    uow = Mock(spec=UoW)
    return CreateCategory(category_service, category_gateway, id_provider, uow)


@pytest.mark.asyncio
async def test_create_operation(interactor: CreateCategory, category_info: NewCategoryDTO, category_id: CategoryId) -> None:
    assert await interactor(category_info) == category_id
