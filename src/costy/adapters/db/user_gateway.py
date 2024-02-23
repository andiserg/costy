from adaptix import Retort
from sqlalchemy import Table, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from costy.application.common.user_gateway import UserReader, UserSaver
from costy.domain.exceptions.access import AuthenticationError
from costy.domain.models.user import User, UserId


class UserGateway(UserSaver, UserReader):
    def __init__(self, session: AsyncSession, table: Table, retort: Retort):
        self.session = session
        self.table = table
        self.retort = retort

    async def save_user(self, user: User) -> None:
        values = self.retort.dump(user)
        del values["id"]
        query = insert(self.table).values(**values)
        result = await self.session.execute(query)
        user.id = result.inserted_primary_key[0]

    async def get_user_by_id(self, user_id: UserId) -> User | None:
        query = select(self.table).where(self.table.c.id == user_id)
        result = await self.session.execute(query)
        data = next(result.mappings(), None)
        return self.retort.load(data, User) if data else None

    async def get_user_id_by_auth_id(self, auth_id: str) -> UserId:
        query = select(self.table).where(self.table.c.auth_id == auth_id)
        result = await self.session.execute(query)
        data = next(result.mappings(), None)
        if data:
            return UserId(data["id"])
        raise AuthenticationError("Invalid auth sub. User is not exists.")
