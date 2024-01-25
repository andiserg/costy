from abc import abstractmethod
from typing import Protocol

from costy.domain.models.user import User, UserId


class UserReader(Protocol):
    @abstractmethod
    async def get_user(self, user_id: UserId) -> User | None:
        raise NotImplementedError


class UserSaver(Protocol):
    @abstractmethod
    async def save_user(self, user: User) -> None:
        raise NotImplementedError
