from sqlalchemy import delete, select
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

    async def get_operation(
            self, operation_id: OperationId
    ) -> Operation | None:
        query = select(Operation).where(
            Operation.id == operation_id  # type: ignore
        )
        result: Operation | None = await self.session.scalar(query)
        return result

    async def save_operation(self, operation: Operation) -> None:
        self.session.add(operation)
        await self.session.flush(objects=[operation])

    async def delete_operation(self, operation_id: OperationId) -> None:
        query = delete(Operation).where(
            Operation.id == operation_id  # type: ignore
        )
        await self.session.execute(query)

    async def find_operations_by_user(
        self, user_id: UserId, from_time: int | None, to_time: int | None
    ) -> list[Operation]:
        query = (
            select(Operation)
            .where(Operation.user_id == user_id)  # type: ignore
        )
        if from_time:
            query = query.where(Operation.time >= from_time)  # type: ignore
        if to_time:
            query = query.where(Operation.time <= to_time)  # type: ignore
        return list(await self.session.scalars(query))
