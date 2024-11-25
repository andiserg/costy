from abc import abstractmethod
from typing import Protocol, runtime_checkable


@runtime_checkable
class IdProvider(Protocol):
    @abstractmethod
    async def get_current_user_id(self) -> int:
        raise NotImplementedError
