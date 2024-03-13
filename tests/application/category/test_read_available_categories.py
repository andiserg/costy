from unittest.mock import Mock

import pytest
from pytest_asyncio import fixture

from costy.application.category.read_available_categories import (
    ReadAvailableCategories,
)
from costy.application.common.category.category_gateway import CategoriesReader
from costy.application.common.uow import UoW


@fixture
async def interactor(id_provider, category_list) -> ReadAvailableCategories:
    category_service = Mock()
    category_gateway = Mock(spec=CategoriesReader)
    category_gateway.find_categories.return_value = category_list
    uow = Mock(spec=UoW)
    return ReadAvailableCategories(category_service, category_gateway, id_provider, uow)


@pytest.mark.asyncio
async def test_read_list_operation(interactor, category_list):
    assert await interactor() == category_list
