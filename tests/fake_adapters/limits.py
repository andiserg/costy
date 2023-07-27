from src.app.repositories.absctract.limits import ALimitRepository
from tests.fake_adapters.base import FakeRepository


class FakeLimitRepository(FakeRepository, ALimitRepository):
    async def get(self, **kwargs):
        pass

    async def get_all(self, user_id: int):
        return []

    async def delete(self, limit_id: int):
        pass
