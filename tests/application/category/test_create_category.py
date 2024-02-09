from unittest.mock import Mock

import pytest
from pytest import fixture

from costy.application.category.create_category import (
    CreateCategory,
    NewCategoryDTO,
)
from costy.application.common.category_gateway import CategorySaver
from costy.application.common.uow import UoW
from costy.domain.models.category import Category, CategoryType


@fixture
def category_info() -> NewCategoryDTO:
    return NewCategoryDTO("test")


@fixture
def interactor(id_provider, category_id, user_id, category_info) -> CreateCategory:
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
async def test_create_operation(interactor: CreateCategory, category_info: NewCategoryDTO, category_id) -> None:
    assert await interactor(category_info) == category_id