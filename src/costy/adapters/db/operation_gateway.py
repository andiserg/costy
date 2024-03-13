from adaptix import Retort, name_mapping
from sqlalchemy import Table, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from costy.application.common.operation.operation_gateway import (
    OperationDeleter,
    OperationReader,
    OperationSaver,
    OperationsBulkSaver,
    OperationsReader,
)
from costy.domain.models.operation import Operation, OperationId
from costy.domain.models.user import UserId


class OperationGateway(OperationReader, OperationSaver, OperationDeleter, OperationsReader, OperationsBulkSaver):
    def __init__(self, session: AsyncSession, table: Table, retort: Retort):
        self.session = session
        self.table = table
        self.retort = retort

    async def get_operation(self, operation_id: OperationId) -> Operation | None:
        query = select(self.table).where(self.table.c.id == operation_id)
        result = await self.session.execute(query)
        data = next(result.mappings(), None)
        return self.retort.load(data, Operation) if data else None

    async def save_operation(self, operation: Operation) -> None:
        values = self.retort.dump(operation)
        del values["id"]
        query = insert(self.table).values(**values)
        result = await self.session.execute(query)
        operation.id = OperationId(result.inserted_primary_key[0])

    async def save_operations(self, operations: list[Operation]) -> None:
        retort = self.retort.extend(recipe=[name_mapping(Operation, skip=["id"])])
        values = retort.dump(operations, list[Operation])
        stmt = insert(self.table).values(values)
        await self.session.execute(stmt)

    async def delete_operation(self, operation_id: OperationId) -> None:
        query = delete(self.table).where(self.table.c.id == operation_id)
        await self.session.execute(query)

    async def find_operations_by_user(
        self,
        user_id: UserId,
        from_time: int | None = None,
        to_time: int | None = None
    ) -> list[Operation]:
        query = select(self.table).where(self.table.c.user_id == user_id)
        if from_time:
            query = query.where(self.table.c.time >= from_time)
        if to_time:
            query = query.where(self.table.c.time <= to_time)
        result = await self.session.execute(query)
        return self.retort.load(result.mappings(), list[Operation])

    async def update_operation(self, operation_id: OperationId, operation: Operation) -> None:
        values = self.retort.dump(operation)

        if not values:
            return

        query = update(self.table).where(self.table.c.id == operation_id).values(**values)
        await self.session.execute(query)
