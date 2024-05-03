import pytest
from adaptix import P, loader, name_mapping
from litestar.testing import AsyncTestClient
from sqlalchemy import insert, select

from costy.domain.models.category import Category, CategoryType
from tests.common.database import create_user


@pytest.mark.asyncio()
async def test_create_category(app, db_session, db_tables, auth_sub, clean_up_db):
    await create_user(db_session, db_tables["users"], auth_sub)

    async with AsyncTestClient(app) as client:
        headers = {"Authorization": "Bearer aboba"}
        data = {
            "name": "test",
        }
        result = await client.post("/categories", json=data, headers=headers)

        assert result.status_code == 201
        assert isinstance(result.json(), int)


@pytest.mark.asyncio()
async def test_get_list_categories(
    app,
    db_session,
    db_tables,
    auth_sub,
    retort,
    clean_up_db,
):
    user_id = await create_user(db_session, db_tables["users"], auth_sub)

    loader_retort = retort.extend(recipe=[loader(P[Category].id, lambda _: None)])
    retort = retort.extend(recipe=[name_mapping(Category, skip=["id"])])

    categories = [
        Category(
            id=None,
            name=f"test_category {i}",
            kind=CategoryType.PERSONAL.value,
            user_id=user_id,
        ) for i in range(5)
    ] + [
        Category(
            id=None,
            name=f"test_category {i}",
            kind=CategoryType.GENERAL.value,
        ) for i in range(5)
    ]
    stmt = insert(db_tables["categories"]).values(retort.dump(categories, list[Category]))
    await db_session.execute(stmt)
    await db_session.commit()

    async with AsyncTestClient(app) as client:
        headers = {"Authorization": "Bearer aboba"}

        result = await client.get("/categories", headers=headers)

        assert loader_retort.load(result.json(), list[Category]) == categories


@pytest.mark.asyncio()
async def test_delete_category(
    app,
    db_session,
    db_tables,
    auth_sub,
    retort,
    clean_up_db,
):
    user_id = await create_user(db_session, db_tables["users"], auth_sub)

    category = Category(
        id=None,
        name="test_category",
        user_id=user_id,
        kind=CategoryType.PERSONAL.value,
    )
    retort = retort.extend(recipe=[name_mapping(Category, skip=["id"])])

    stmt = insert(db_tables["categories"]).values(retort.dump(category))
    created_category_id = (await db_session.execute(stmt)).inserted_primary_key[0]
    await db_session.commit()

    async with AsyncTestClient(app) as client:
        headers = {"Authorization": "Bearer aboba"}

        result = await client.delete(f"/categories/{created_category_id}", headers=headers)

        assert result.status_code == 204

    stmt = select(db_tables["categories"]).where(db_tables["categories"].c.id == created_category_id)
    result = list(await db_session.execute(stmt))

    assert result == []


@pytest.mark.asyncio()
async def test_update_category(
    app,
    db_session,
    db_tables,
    auth_sub,
    retort,
    clean_up_db,
):
    user_id = await create_user(db_session, db_tables["users"], auth_sub)

    category = Category(
        id=None,
        name="test_category",
        user_id=user_id,
        kind=CategoryType.PERSONAL.value,
    )
    retort = retort.extend(recipe=[name_mapping(Category, skip=["id"])])

    dumped_category = retort.dump(category)
    stmt = insert(db_tables["categories"]).values(dumped_category)
    created_category_id = (await db_session.execute(stmt)).inserted_primary_key[0]
    await db_session.commit()

    update_data = {"name": "upd_test_category"}

    async with AsyncTestClient(app) as client:
        headers = {"Authorization": "Bearer aboba"}

        result = await client.put(f"/categories/{created_category_id}", headers=headers, json=update_data)

        assert result.status_code == 200

    dumped_category["name"] = update_data["name"]
    dumped_category["id"] = created_category_id

    stmt = select(db_tables["categories"]).where(db_tables["categories"].c.id == created_category_id)
    result = next((await db_session.execute(stmt)).mappings(), None)

    assert result == dumped_category
