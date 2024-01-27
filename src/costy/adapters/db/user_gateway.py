from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from costy.application.common.user_gateway import UserReader, UserSaver
from costy.domain.models.user import User, UserId


class UserGateway(UserSaver, UserReader):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_user(self, user: User) -> None:
        self.session.add(user)
        await self.session.flush(objects=[user])

    async def get_user_by_id(self, user_id: UserId) -> User | None:
        query = select(User).where(User.id == user_id)
        return await self.session.scalar(query)

    async def get_user_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        return await self.session.scalar(query)