from sqlalchemy import select

from src.app.adapters.repository import SqlAlchemyRepository
from src.app.operations.models import Operation


class OperationRepository(SqlAlchemyRepository):
    async def get(self, field, value) -> Operation:
        return await self._get(Operation, field, value)

    async def get_all_by_user(self, user_id) -> list[Operation]:
        return list(
            await self.session.scalars(select(Operation).filter_by(user_id=user_id))
        )
