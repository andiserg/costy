from abc import ABC, abstractmethod


class FakeRepository(ABC):
    def __init__(self):
        self.instances = []

    @abstractmethod
    async def get(self, **kwargs):
        raise NotImplementedError

    async def add(self, instance):
        self.instances.append(instance)

    async def _get(self, **kwargs):
        result = list(
            filter(
                lambda instance: all(
                    [
                        instance.__dict__[prop] == value
                        for (prop, value) in kwargs.items()
                    ]
                ),
                self.instances,
            )
        )
        return result[0] if result else None
