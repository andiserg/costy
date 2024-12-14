import logging

from adaptix import Retort
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth import tables
from auth.application._common import UserReader, UserSaver
from auth.exceptions import AuthenticationError
from auth.models import User, UserId

logger = logging.getLogger(__name__)
retort = Retort()


class UserAdapter(UserSaver, UserReader):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.table = tables.users
        self.retort = retort

    async def save_user(self, user: User) -> None:
        values = self.retort.dump(user)
        del values["id"]
        stmt = insert(self.table).values(**values)
        result = await self.session.execute(stmt)
        user.id = result.inserted_primary_key[0]

    async def get_user_by_id(self, user_id: UserId) -> User | None:
        stmt = select(self.table).where(self.table.c.id == user_id)
        result = await self.session.execute(stmt)
        data = next(result.mappings(), None)
        if data:
            return self.retort.load(data, User)
        logger.error("No user found with id %s", user_id)
        return None

    async def get_user_by_auth_id(self, auth_id: str) -> User:
        stmt = select(self.table).where(self.table.c.auth_id == auth_id)
        result = await self.session.execute(stmt)
        data = next(result.mappings(), None)
        if data:
            return self.retort.load(data, User)
        logger.error("No user found with auth id %s", auth_id)
        raise AuthenticationError("Invalid auth sub. User is not exists.")
