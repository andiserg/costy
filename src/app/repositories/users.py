from src.app.domain.users import User
from src.app.repositories.absctract.users import AUserRepository
from src.app.repositories.sqlalchemy import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository, AUserRepository):
    async def get(self, field, value) -> User:
        return await self._get(User, field, value)
