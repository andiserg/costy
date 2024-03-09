from abc import abstractmethod
from typing import Protocol, runtime_checkable

from ...domain.models.user import UserId


@runtime_checkable
class IdProvider(Protocol):
    @abstractmethod
    async def get_current_user_id(self) -> UserId:
        raise NotImplementedError
