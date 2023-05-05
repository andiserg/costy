from abc import ABC, abstractmethod


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
