from src.app.domain.users import User
from src.app.repositories.absctract.users import AUserRepository
from tests.fake_adapters.base import FakeRepository


class FakeUserRepository(FakeRepository, AUserRepository):
    async def get(self, **kwargs) -> User | None:
        return await self._get(**kwargs)
