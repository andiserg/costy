from abc import abstractmethod
from typing import Protocol, runtime_checkable


@runtime_checkable
class Commiter(Protocol):
    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError
