import pytest
from adaptix import P, loader, name_mapping
from litestar.testing import AsyncTestClient
from sqlalchemy import insert, select

from costy.domain.models.category import Category, CategoryType


@pytest.mark.asyncio
async def test_create_category(app, user_token, create_sub_user, clean_up_db):
    async with AsyncTestClient(app) as client:
        headers = {"Authorization": f"Bearer {user_token}"}
        data = {
            "name": "test"
        }
        result = await client.post("/categories", json=data, headers=headers)

        assert result.status_code == 201
        assert isinstance(result.json(), int)


@pytest.mark.asyncio
async def test_get_list_categoris(
    app,
    user_token,
    create_sub_user,
    db_session,
    db_tables,
    retort,
    clean_up_db
):
    loader_retort = retort.extend(
        recipe=[
            loader(P[Category].id, lambda _: None)
        ]
    )
    retort = retort.extend(
        recipe=[
            name_mapping(
                Category,
                skip=['id'],
            ),
        ]
    )
    categories = [
        Category(
            id=None,
            name=f"test_category {i}",
            kind=CategoryType.PERSONAL.value,
            user_id=create_sub_user
        ) for i in range(5)
    ] + [
        Category(
            id=None,
            name=f"test_category {i}",
            kind=CategoryType.GENERAL.value
        ) for i in range(5)
    ]
    stmt = insert(db_tables["categories"]).values(retort.dump(categories, list[Category]))
    await db_session.execute(stmt)
    await db_session.commit()

    async with AsyncTestClient(app) as client:
        headers = {"Authorization": f"Bearer {user_token}"}

        result = await client.get("/categories", headers=headers)

        assert loader_retort.load(result.json(), list[Category]) == categories


@pytest.mark.asyncio
async def test_delete_category(
    app,
    user_token,
    create_sub_user,
    db_session,
    db_tables,
    retort,
    clean_up_db
):
    category = Category(
        id=None,
        name="test_category",
        user_id=create_sub_user,
        kind=CategoryType.PERSONAL.value
    )
    retort = retort.extend(
        recipe=[
            name_mapping(
                Category,
                skip=['id'],
            ),
        ]
    )
    stmt = insert(db_tables["categories"]).values(retort.dump(category))
    created_category_id = (await db_session.execute(stmt)).inserted_primary_key[0]
    await db_session.commit()

    async with AsyncTestClient(app) as client:
        headers = {"Authorization": f"Bearer {user_token}"}

        result = await client.delete(f"/categories/{created_category_id}", headers=headers)

        assert result.status_code == 204

    stmt = select(db_tables["operations"]).where(db_tables["categories"].c.id == created_category_id)
    assert list(await db_session.execute(stmt)) == []
