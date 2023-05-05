from src.app.domain.users import User
from tests.fake_adapters.base import FakeRepository


class UserRepository(FakeRepository):
    def get(self, prop, value) -> User | None:
        return self._get(prop, value)
