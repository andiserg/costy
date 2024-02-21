from adaptix import Retort
from sqlalchemy import Table, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from costy.application.common.operation_gateway import (
    OperationDeleter,
    OperationReader,
    OperationSaver,
    OperationsReader,
)
from costy.domain.models.operation import Operation, OperationId
from costy.domain.models.user import UserId


class OperationGateway(
    OperationReader, OperationSaver, OperationDeleter, OperationsReader
):
    def __init__(self, session: AsyncSession, table: Table, retort: Retort):
        self.session = session
        self.table = table
        self.retort = retort

    async def get_operation(
            self, operation_id: OperationId
    ) -> Operation | None:
        query = select(self.table).where(
            self.table.c.id == operation_id
        )
        result: Operation | None = await self.session.scalar(query)
        return result

    async def save_operation(self, operation: Operation) -> None:
        self.session.add(operation)
        await self.session.flush(objects=[operation])

    async def delete_operation(self, operation_id: OperationId) -> None:
        query = delete(self.table).where(
            self.table.c.id == operation_id
        )
        await self.session.execute(query)

    async def find_operations_by_user(
        self, user_id: UserId, from_time: int | None, to_time: int | None
    ) -> list[Operation]:
        query = (
            select(self.table)
            .where(self.table.c.user_id == user_id)
        )
        if from_time:
            query = query.where(self.table.c.time >= from_time)
        if to_time:
            query = query.where(self.table.c.time <= to_time)
        return list(await self.session.scalars(query))
