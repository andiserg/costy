from datetime import datetime, timedelta

from sqlalchemy import select

from src.app.domain.operations import Operation
from src.app.repositories.absctract.operations import AOperationRepository
from src.app.repositories.sqlalchemy import SqlAlchemyRepository


class OperationRepository(SqlAlchemyRepository, AOperationRepository):
    async def get(self, field, value) -> Operation:
        return await self._get(Operation, field, value)

    async def get_all_by_user(
        self,
        user_id,
        from_time: int = None,
        to_time: int = None,
    ) -> list[Operation]:
        from_time = (
            from_time
            if from_time
            else int((datetime.now() - timedelta(days=1)).timestamp())
        )
        to_time = to_time if to_time else int(datetime.now().timestamp())
        return list(
            await self.session.scalars(
                select(Operation)
                .filter(Operation.time >= from_time, Operation.time <= to_time)
                .filter_by(user_id=user_id)
            )
        )
