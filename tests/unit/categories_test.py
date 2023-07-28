import pytest

from src.app.domain.categories import Category
from src.app.services.categories import create_category, get_availables_categories
from src.schemas.categories import CategoryCreateSchema
from tests.fake_adapters.uow import FakeUnitOfWork


@pytest.mark.asyncio
async def test_create_category():
    uow = FakeUnitOfWork()
    schema = CategoryCreateSchema(name="Test category", icon_color="", icon_name="")
    category = await create_category(uow, 1, schema)
    assert isinstance(category, Category)


# @pytest.mark.asyncio
# async def test_create_dublicate_category():
#     """
#     Якщо відбувається спроба створити категорію-дублікат,
#     то категорія не створюється, а метод повинен повернути категорію-оригінал
#     :return:
#     """
#     uow = FakeUnitOfWork()
#     schema = CategoryCreateSchema(name="Test category", icon_color="", icon_name="")
#     created_category = await create_category(uow, 1, schema)
#     category = await create_category(uow, 1, schema)
#     assert category == created_category


@pytest.mark.asyncio
async def test_read_availables_categories():
    uow = FakeUnitOfWork()
    uow.categories.instances = [
        Category(
            id=i,
            name=f"Test category #{i}",
            user_id=1,
            type="user",
            icon_color="",
            icon_name="",
        )
        for i in range(10)
    ]
    categories = await get_availables_categories(uow, user_id=1)
    assert len(categories) == 10
