import pytest

from costy.domain.models.category import Category, CategoryType
from costy.domain.models.user import UserId
from tests.common.database import create_user


def create_categories(user_id: UserId) -> tuple[Category, Category]:
    return (
        Category(id=None, name="general category"),
        Category(
            id=None,
            name="user category",
            user_id=user_id,
            kind=CategoryType.PERSONAL.value
        )
    )


@pytest.mark.asyncio
async def test_save_category(category_gateway, db_session, db_tables):
    user_id = await create_user(db_session, db_tables["users"])
    general_category, personal_category = create_categories(user_id)

    await category_gateway.save_category(general_category)
    await category_gateway.save_category(personal_category)

    assert general_category.id is not None
    assert personal_category.id is not None


@pytest.mark.asyncio
async def test_get_category(category_gateway, db_session, db_tables):
    user_id = await create_user(db_session, db_tables["users"])
    general_category, personal_category = create_categories(user_id)
    await category_gateway.save_category(general_category)
    await category_gateway.save_category(personal_category)

    created_general_category = await category_gateway.get_category(general_category.id)
    created_personal_category = await category_gateway.get_category(personal_category.id)

    assert general_category == created_general_category
    assert personal_category == created_personal_category


@pytest.mark.asyncio
async def test_delete_category(category_gateway, db_session, db_tables):
    user_id = await create_user(db_session, db_tables["users"])
    general_category, personal_category = create_categories(user_id)
    await category_gateway.save_category(general_category)
    await category_gateway.save_category(personal_category)

    await category_gateway.delete_category(general_category.id)
    await category_gateway.delete_category(personal_category.id)

    assert await category_gateway.get_category(general_category.id) is None
    assert await category_gateway.get_category(personal_category.id) is None


@pytest.mark.asyncio
async def test_find_categories(category_gateway, db_session, db_tables):
    user_id = await create_user(db_session, db_tables["users"])
    created_categories = []
    for i in range(5):
        category = Category(
            id=None,
            name=f"category {i}",
            user_id=user_id,
        )
        await category_gateway.save_category(category)
        created_categories.append(category)

    categories = await category_gateway.find_categories(user_id)

    assert categories == created_categories


@pytest.mark.asyncio
async def test_update_category(category_gateway, db_session, db_tables):
    user_id = await create_user(db_session, db_tables["users"])
    category = Category(id=None, name="test", user_id=user_id, kind=CategoryType.PERSONAL.value)
    await category_gateway.save_category(category)

    updated_category = Category(
        id=category.id,
        name="upd_test",
        user_id=user_id,
        kind=CategoryType.PERSONAL.value
    )

    await category_gateway.update_category(category.id, updated_category)

    assert await category_gateway.get_category(category.id) == updated_category


@pytest.mark.asyncio
async def test_find_categories_by_mcc(category_gateway, db_session, db_tables):
    mcc_codes = [1, 2]
    categories = [
        Category(
            name=f"test #{mcc_code}",
            kind=CategoryType.BANK.value,
            mcc=mcc_code
        ) for mcc_code in mcc_codes
    ]
    for category in categories:
        await category_gateway.save_category(category)

    result = await category_gateway.find_categories_by_mcc_codes(mcc_codes)

    assert result == {category.mcc: category for category in categories}
