from sqlalchemy import delete, select

from src.app.domain.limits import Limit
from src.app.repositories.absctract.limits import ALimitRepository
from src.app.repositories.sqlalchemy import SqlAlchemyRepository


class LimitRepository(SqlAlchemyRepository, ALimitRepository):
    async def get(self, **kwargs):
        return self._get(Limit, **kwargs)

    async def get_all(self, user_id: int):
        return list(
            await self.session.scalars(select(Limit).filter_by(user_id=user_id))
        )

    async def delete(self, **kwargs):
        await self.session.execute(delete(Limit).filter_by(**kwargs))
