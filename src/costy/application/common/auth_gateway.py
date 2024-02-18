from abc import abstractmethod
from typing import Protocol

from costy.domain.models.user import UserId


class AuthLoger(Protocol):
    @abstractmethod
    async def authenticate(self, email: str, password: str) -> str | None:
        raise NotImplementedError

    @abstractmethod
    async def get_user_id_by_sub(self, sub: str) -> UserId:
        raise NotImplementedError
