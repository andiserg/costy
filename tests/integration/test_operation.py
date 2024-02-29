import pytest
from adaptix import P, loader, name_mapping
from litestar.testing import AsyncTestClient
from sqlalchemy import insert

from costy.domain.models.operation import Operation


@pytest.mark.asyncio
async def test_create_operation(app, user_token, create_sub_user, db_category_id, clean_up_db):
    async with AsyncTestClient(app) as client:
        headers = {"Authorization": f"Bearer {user_token}"}
        data = {
            "amount": 100,
            "category_id": db_category_id
        }
        result = await client.post("/operations", json=data, headers=headers)

        assert result.status_code == 201
        assert isinstance(result.json(), int)


@pytest.mark.asyncio
async def test_get_list_operations(
    app,
    user_token,
    create_sub_user,
    db_session,
    db_tables,
    db_category_id,
    retort,
    clean_up_db
):
    loader_retort = retort.extend(
        recipe=[
            loader(P[Operation].id, lambda _: None)
        ]
    )
    retort = retort.extend(
        recipe=[
            name_mapping(
                Operation,
                skip=['id'],
            ),
        ]
    )
    operations = [
        Operation(
            id=None,
            amount=100,
            description="test",
            category_id=db_category_id,
            time=1111,
            user_id=create_sub_user
        )
        for _ in range(10)
    ]
    stmt = insert(db_tables["operations"]).values(retort.dump(operations, list[Operation]))
    await db_session.execute(stmt)
    await db_session.commit()

    async with AsyncTestClient(app) as client:
        headers = {"Authorization": f"Bearer {user_token}"}

        result = await client.get("/operations", headers=headers)

        assert loader_retort.load(result.json(), list[Operation]) == operations
