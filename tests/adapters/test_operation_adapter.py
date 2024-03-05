import pytest
from sqlalchemy import Table
from sqlalchemy.ext.asyncio import AsyncSession

from costy.domain.models.category import CategoryId
from costy.domain.models.operation import Operation
from costy.domain.models.user import UserId
from tests.common.database import create_category, create_user


async def create_operation_depends(
        session: AsyncSession,
        tables: dict[str, Table]
) -> tuple[UserId, CategoryId]:
    return await create_user(session, tables["users"]), await create_category(session, tables["categories"])


def create_operation(user_id, category_id) -> Operation:
    return Operation(
        id=None,
        amount=100,
        description="desc",
        category_id=category_id,
        user_id=user_id,
        time=11111
    )


@pytest.mark.asyncio
async def test_save_operation(operation_gateway, db_session, db_tables):
    user_id, category_id = await create_operation_depends(db_session, db_tables)
    operation = create_operation(user_id, category_id)

    await operation_gateway.save_operation(operation)

    assert operation.id is not None


@pytest.mark.asyncio
async def test_get_operation(operation_gateway, db_session, db_tables):
    user_id, category_id = await create_operation_depends(db_session, db_tables)
    operation = create_operation(user_id, category_id)
    await operation_gateway.save_operation(operation)
    created_operation_id = operation.id

    result_operation = await operation_gateway.get_operation(created_operation_id)

    assert result_operation == operation


@pytest.mark.asyncio
async def test_delete_operation(operation_gateway, db_session, db_tables):
    user_id, category_id = await create_operation_depends(db_session, db_tables)
    operation = create_operation(user_id, category_id)
    await operation_gateway.save_operation(operation)
    created_operation_id = operation.id

    await operation_gateway.delete_operation(created_operation_id)

    assert await operation_gateway.get_operation(created_operation_id) is None


@pytest.mark.asyncio
async def test_find_operations_by_user(operation_gateway, db_session, db_tables):
    user_id, category_id = await create_operation_depends(db_session, db_tables)
    created_operations = []
    for i in range(5):
        operation = Operation(
            id=None,
            amount=100*i,
            description=f"desc #{i}",
            category_id=category_id,
            user_id=user_id,
            time=1111
        )
        await operation_gateway.save_operation(operation)
        created_operations.append(operation)

    operations = await operation_gateway.find_operations_by_user(user_id)

    assert operations == created_operations


@pytest.mark.asyncio
async def test_update_operation(operation_gateway, db_session, db_tables):
    user_id, category_id = await create_operation_depends(db_session, db_tables)
    operation = create_operation(user_id, category_id)
    await operation_gateway.save_operation(operation)

    updated_operation = Operation(
        id=operation.id,
        amount=200,
        description="test data",
        category_id=category_id,
        time=2222,
        user_id=user_id
    )

    await operation_gateway.update_operation(operation.id, updated_operation)

    assert await operation_gateway.get_operation(operation.id) == updated_operation
