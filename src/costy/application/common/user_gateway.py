from abc import abstractmethod
from typing import Protocol

from costy.domain.models.user import UserId, User


class UserReader(Protocol):
    @abstractmethod
    def get_user(self, user_id: UserId) -> User:
        raise NotImplementedError


class UserSaver(Protocol):
    @abstractmethod
    async def save_user(self, user: User) -> None:
        raise NotImplementedError
