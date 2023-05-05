from src.app.domain.operations import Operation
from tests.fake_adapters.base import FakeRepository


class OperationRepository(FakeRepository):
    def get(self, prop, value) -> Operation | None:
        return self._get(prop, value)

    def get_all_by_user(self, user_id, from_time: int, to_time: int) -> list[Operation]:
        return list(
            filter(
                lambda instance: instance.user_id == user_id
                and from_time < instance.time < to_time,
                self.instances,
            )
        )
