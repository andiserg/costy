import pytest
from adaptix import P, loader, name_mapping
from litestar.testing import AsyncTestClient
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from costy.domain.models.category import CategoryId
from costy.domain.models.operation import Operation
from costy.infrastructure.db import tables
from tests.common.crud import create_category


async def create_depends(
    session: AsyncSession,
) -> CategoryId:
    return await create_category(session)


@pytest.mark.asyncio()
async def test_create_operation(costy_app, db_session, db_tables, clean_up_db):
    category_id = await create_depends(db_session)

    async with AsyncTestClient(app=costy_app) as client:
        headers = {"user_id": "1"}

        data = {
            "amount": 100,
            "category_id": category_id,
        }
        result = await client.post("/operations", json=data, headers=headers)

        assert result.status_code == 201
        assert isinstance(result.json(), int)


@pytest.mark.asyncio()
async def test_get_list_operations(
    costy_app,
    db_session,
    db_tables,
    retort,
    clean_up_db,
):
    category_id = await create_depends(db_session)

    loader_retort = retort.extend(recipe=[loader(P[Operation].id, lambda _: None)])
    retort = retort.extend(recipe=[name_mapping(Operation, skip=["id"])])

    operations = [
        Operation(
            id=None,
            amount=100,
            description="test",
            category_id=category_id,
            time=1111,
            user_id=1,
        )
        for _ in range(10)
    ]
    stmt = insert(tables.operations).values(retort.dump(operations, list[Operation]))
    await db_session.execute(stmt)
    await db_session.commit()

    async with AsyncTestClient(costy_app) as client:
        headers = {"user_id": "1"}

        result = await client.get("/operations", headers=headers)

        assert loader_retort.load(result.json(), list[Operation]) == operations


async def create_operation(user_id, category_id, session: AsyncSession, retort):
    operation = Operation(
        id=None,
        amount=100,
        description="test",
        category_id=category_id,
        time=1111,
        user_id=user_id,
    )
    retort = retort.extend(
        recipe=[
            name_mapping(
                Operation,
                skip=["id"],
            ),
        ],
    )
    stmt = insert(tables.operations).values(retort.dump(operation))
    operation_id = (await session.execute(stmt)).inserted_primary_key[0]
    await session.commit()
    return operation_id


@pytest.mark.asyncio()
async def test_delete_operation_own(
    costy_app,
    db_session,
    db_tables,
    retort,
    clean_up_db,
):
    category_id = await create_depends(db_session)
    created_operation_id = await create_operation(1, category_id, db_session, retort)

    async with AsyncTestClient(costy_app) as client:
        headers = {"user_id": "1"}

        result = await client.delete(f"/operations/{created_operation_id}", headers=headers)

        assert result.status_code == 204

    stmt = select(tables.operations).where(tables.operations.c.id == created_operation_id)
    result = list(await db_session.execute(stmt))

    assert result == []


@pytest.mark.asyncio()
@pytest.mark.skip()
async def test_delete_operation_someone(
    costy_app,
    db_session,
    auth_sub,
    retort,
    clean_up_db,
):
    category_id = await create_depends(db_session)
    operation_id = await create_operation(2, category_id, db_session, retort)

    async with AsyncTestClient(costy_app) as client:
        headers = {"user_id": "1"}

        result = await client.delete(f"/operations/{operation_id}", headers=headers)

        assert result.status_code == 403

    stmt = select(tables.operations).where(tables.operations.c.id == operation_id)
    result = list(await db_session.execute(stmt))

    assert result != []


@pytest.mark.skip()
@pytest.mark.asyncio()
async def test_delete_operation_not_exists(
    costy_app,
    db_session,
    retort,
    clean_up_db,
):
    category_id = await create_depends(db_session)
    operation_id = await create_operation(1, category_id, db_session, retort)

    async with AsyncTestClient(costy_app) as client:
        headers = {"user_id": "1"}

        result = await client.delete("/operations/9999", headers=headers)


        assert result.status_code == 400

    stmt = select(tables.operations).where(tables.operations.c.id == operation_id)
    result = list(await db_session.execute(stmt))

    assert result != []
