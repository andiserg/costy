from sqlalchemy import select, delete
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
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_operation(self, operation_id: OperationId) -> Operation:
        query = select(Operation).where(Operation.id == operation_id)
        return await self.session.scalar(query)

    async def save_operation(self, operation: Operation) -> None:
        self.session.add(operation)
        await self.session.flush(objects=[operation])

    async def delete_operation(self, operation_id: OperationId) -> None:
        query = delete(Operation).where(Operation.id == operation_id)
        await self.session.execute(query)

    async def find_operations_by_user(
        self, user_id: UserId, from_time: int, to_time: int
    ) -> list[Operation]:
        query = (
            select(Operation)
            .where(Operation.user_id == user_id)
            .where(Operation.time >= from_time, Operation.time <= to_time)
        )
        return list(await self.session.scalars(query))
