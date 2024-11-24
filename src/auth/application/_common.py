from abc import abstractmethod
from typing import Generic, Protocol, TypeVar, runtime_checkable

from auth.models import User, UserId

InputDTO = TypeVar("InputDTO")
OutputDTO = TypeVar("OutputDTO")


class Interactor(Generic[InputDTO, OutputDTO]):
    async def __call__(self, data: InputDTO) -> OutputDTO:
        raise NotImplementedError


@runtime_checkable
class Commiter(Protocol):
    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError


@runtime_checkable
class UserProvider(Protocol):
    @abstractmethod
    async def get_user_by_token(self, token: str) -> User:
        raise NotImplementedError


@runtime_checkable
class UserSaver(Protocol):
    @abstractmethod
    async def save_user(self, user: User) -> None:
        raise NotImplementedError


@runtime_checkable
class UserReader(Protocol):
    @abstractmethod
    async def get_user_by_id(self, user_id: UserId) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_auth_id(self, auth_id: str) -> User:
        raise NotImplementedError


class AuthLoger(Protocol):
    @abstractmethod
    async def authenticate(self, email: str, password: str) -> str | None:
        raise NotImplementedError


class AuthRegister(Protocol):
    @abstractmethod
    async def register(self, email: str, password: str) -> str:
        raise NotImplementedError
