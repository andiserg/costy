from abc import ABC, abstractmethod

from src.app.account.users.models import User
from src.app.operations.models import Operation


class FakeRepository(ABC):
    def __init__(self):
        self.instances = []

    @abstractmethod
    def get(self, prop, value):
        raise NotImplementedError

    def add(self, instance):
        self.instances.append(instance)

    def _get(self, prop, value):
        result = list(
            filter(lambda instance: instance.__dict__()[prop] == value, self.instances)
        )
        return result[0] if result else None


class UserRepository(FakeRepository):
    def get(self, prop, value) -> User | None:
        return self._get(prop, value)


class OperationRepository(FakeRepository):
    def get(self, prop, value) -> Operation | None:
        return self._get(prop, value)

    def get_all_by_user(self, user_id) -> list[Operation]:
        return list(
            filter(lambda instance: instance.user_id == user_id, self.instances)
        )
