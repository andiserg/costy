from src.app.account.users.models import User
from src.app.adapters.repository import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):
    async def get(self, field, value) -> User:
        return await self._get(User, field, value)
