from src.app.domain.operations import Operation
from src.app.repositories.absctract.operations import AOperationRepository
from tests.fake_adapters.base import FakeRepository


class FakeOperationRepository(FakeRepository, AOperationRepository):
    async def get(self, **kwargs) -> Operation | None:
        return await self._get(**kwargs)

    async def get_all_by_user(
        self, user_id, from_time: int, to_time: int
    ) -> list[Operation]:
        return list(
            filter(
                lambda instance: instance.user_id == user_id
                and from_time < instance.time < to_time,
                self.instances,
            )
        )
