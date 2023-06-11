from src.app.domain.limits import Limit
from src.app.repositories.absctract.limits import ALimitRepository
from src.app.repositories.sqlalchemy import SqlAlchemyRepository


class LimitRepository(SqlAlchemyRepository, ALimitRepository):
    async def get(self, **kwargs):
        return self._get(Limit, **kwargs)

    async def get_all(self, user_id: int):
        pass

    async def delete(self, limit_id: int):
        pass
