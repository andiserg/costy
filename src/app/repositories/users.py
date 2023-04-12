from src.app.models.users import User
from src.app.repositories.sqlalchemy import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):
    async def get(self, field, value) -> User:
        return await self._get(User, field, value)
