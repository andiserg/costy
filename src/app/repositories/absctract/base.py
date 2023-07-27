from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    async def add(self, model_object):
        raise NotImplementedError

    @abstractmethod
    async def get(self, **kwargs):
        raise NotImplementedError
