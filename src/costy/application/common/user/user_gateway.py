from abc import abstractmethod
from typing import Protocol, runtime_checkable

from costy.domain.models.user import User, UserId


@runtime_checkable
class UserReader(Protocol):
    @abstractmethod
    async def get_user_by_id(self, user_id: UserId) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_user_id_by_auth_id(self, auth_id: str) -> UserId:
        raise NotImplementedError


@runtime_checkable
class UserSaver(Protocol):
    @abstractmethod
    async def save_user(self, user: User) -> None:
        raise NotImplementedError
