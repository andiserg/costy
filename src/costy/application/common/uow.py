from abc import abstractmethod
from typing import Protocol, runtime_checkable


@runtime_checkable
class UoW(Protocol):
    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def flush(self) -> None:
        raise NotImplementedError
