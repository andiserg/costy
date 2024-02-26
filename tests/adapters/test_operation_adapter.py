import pytest
from pytest_asyncio import fixture
from sqlalchemy import insert

from costy.adapters.db.operation_gateway import OperationGateway
from costy.domain.models.category import CategoryId
from costy.domain.models.operation import Operation
from costy.domain.models.user import UserId


@fixture
async def operation_gateway(db_session, db_tables, retort) -> OperationGateway:
    return OperationGateway(db_session, db_tables["operations"], retort)


@fixture()
async def db_user_id(db_session, db_tables) -> UserId:
    created_user_record = await db_session.execute(insert(db_tables["users"]).values(auth_id="test"))
    return UserId(created_user_record.inserted_primary_key[0])


@fixture
async def db_category_id(db_session, db_tables) -> CategoryId:
    created_category_record = await db_session.execute(insert(db_tables["categories"]).values(name="test"))
    return CategoryId(created_category_record.inserted_primary_key[0])


@fixture
async def operation_entity(db_user_id, db_category_id) -> Operation:
    return Operation(
        id=None,
        amount=100,
        description="desc",
        category_id=db_category_id,
        user_id=db_user_id,
        time=11111
    )


@pytest.mark.asyncio
async def test_save_operation(operation_gateway, db_session, db_tables, operation_entity):
    await operation_gateway.save_operation(operation_entity)

    assert operation_entity.id is not None


@pytest.mark.asyncio
async def test_get_operation(operation_gateway, db_session, db_tables, operation_entity):
    await operation_gateway.save_operation(operation_entity)
    created_operation_id = operation_entity.id

    operation = await operation_gateway.get_operation(created_operation_id)

    assert operation_entity == operation


@pytest.mark.asyncio
async def test_delete_operation(operation_gateway, db_session, db_tables, operation_entity):
    await operation_gateway.save_operation(operation_entity)
    created_operation_id = operation_entity.id

    await operation_gateway.delete_operation(created_operation_id)

    assert await operation_gateway.get_operation(created_operation_id) is None


@pytest.mark.asyncio
async def test_find_operations_by_user(operation_gateway, db_session, db_tables, db_category_id, db_user_id):
    created_operations = []
    for i in range(5):
        operation = Operation(
            id=None,
            amount=100*i,
            description=f"desc #{i}",
            category_id=db_category_id,
            user_id=db_user_id,
            time=1111
        )
        await operation_gateway.save_operation(operation)
        created_operations.append(operation)

    operations = await operation_gateway.find_operations_by_user(db_user_id)

    assert operations == created_operations
