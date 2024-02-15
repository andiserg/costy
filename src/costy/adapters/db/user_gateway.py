from adaptix import Retort
from sqlalchemy import Table, select
from sqlalchemy.ext.asyncio import AsyncSession

from costy.application.common.user_gateway import UserReader, UserSaver
from costy.domain.models.user import User, UserId


class UserGateway(UserSaver, UserReader):
    def __init__(self, session: AsyncSession, table: Table, retort: Retort):
        self.session = session
        self.table = table
        self.retort = retort

    async def save_user(self, user: User) -> None:
        self.session.add(user)
        await self.session.flush(objects=[user])

    async def get_user_by_id(self, user_id: UserId) -> User | None:
        query = select(self.table).where(self.table.c.id == user_id)
        result: User | None = await self.session.scalar(query)
        return result

    async def get_user_by_auth_id(self, auth_id: str) -> User | None:
        query = select(self.table).where(self.table.c.auth_id == auth_id)
        result = await self.session.scalar(query)
        return result
