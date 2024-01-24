from abc import abstractmethod
from typing import Protocol

from costy.domain.models.user import UserId


class IdProvider(Protocol):
    @abstractmethod
    async def get_current_user_id(self) -> UserId:
        raise NotImplementedError
