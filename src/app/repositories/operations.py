from sqlalchemy import select

from src.app.domain.operations import Operation
from src.app.repositories.absctract.operations import AOperationRepository
from src.app.repositories.sqlalchemy import SqlAlchemyRepository


class OperationRepository(SqlAlchemyRepository, AOperationRepository):
    async def get(self, **kwargs) -> Operation:
        return await self._get(Operation, **kwargs)

    async def get_all_by_user(
        self, user_id, from_time: int, to_time: int
    ) -> list[Operation]:
        return list(
            await self.session.scalars(
                select(Operation)
                .filter(Operation.time >= from_time, Operation.time <= to_time)
                .filter_by(user_id=user_id)
            )
        )

    async def delete(self, **kwargs):
        await self._delete(Operation, **kwargs)
