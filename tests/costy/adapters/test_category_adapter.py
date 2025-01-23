import pytest
from sqlalchemy import insert

from costy.domain.models.category import Category, CategoryType
from costy.infrastructure.db import tables


def create_categories(user_id: int) -> tuple[Category, Category]:
    return (
        Category(id=None, name="general category"),
        Category(
            id=None,
            name="user category",
            user_id=user_id,
            kind=CategoryType.PERSONAL.value,
        ),
    )


@pytest.mark.asyncio()
@pytest.mark.parametrize("category", create_categories(1))
async def test_save_category(category, category_gateway, db_session):
    await category_gateway.save_category(category)
    assert category.id is not None


@pytest.mark.asyncio()
@pytest.mark.parametrize("category", create_categories(1))
async def test_get_category(category, category_gateway, db_session):
    await category_gateway.save_category(category)
    assert category == await category_gateway.get_category_by_id(category.id)


@pytest.mark.asyncio()
@pytest.mark.parametrize("category", create_categories(1))
async def test_delete_category(category, category_gateway, db_session):
    await category_gateway.save_category(category)
    await category_gateway.delete_category(category.id)
    assert await category_gateway.get_category_by_id(category.id) is None


@pytest.mark.asyncio()
async def test_update_category(category_gateway, db_session):
    category = Category(id=None, name="test", user_id=1)
    await category_gateway.save_category(category)

    upd_category = Category(id=category.id, name="upd_test", user_id=1)
    await category_gateway.update_category(category.id, upd_category)

    assert await category_gateway.get_category_by_id(category.id) == upd_category


@pytest.mark.asyncio()
async def test_find_categories(category_gateway, db_session):
    created_categories = []
    for i in range(5):
        category = Category(id=None, name=f"category {i}", user_id=1)
        await category_gateway.save_category(category)
        created_categories.append(category)

    categories = await category_gateway.find_categories(1)

    assert categories == created_categories


@pytest.mark.asyncio()
async def test_find_categories_by_mcc(category_gateway, db_session):
    mcc_codes = [1, 2]
    categories = [
        Category(name=f"test #{mcc_code}", kind=CategoryType.GENERAL.value)
        for mcc_code in mcc_codes
    ]
    for category in categories:
        await category_gateway.save_category(category)

    # link categories to mcc
    await db_session.execute(
        insert(tables.category_mcc),
        [
            {"category_id": c.id, "mcc": mcc}
            for c, mcc in zip(categories, mcc_codes)
        ],
    )

    # add mcc without categories to mcc codes
    mcc_codes.append(3)

    result = await category_gateway.find_categories_by_mcc_codes(mcc_codes)

    assert result == {mcc: category for category, mcc in zip(categories, mcc_codes)}
