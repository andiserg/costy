from abc import abstractmethod
from typing import Protocol


class AuthLoger(Protocol):
    @abstractmethod
    async def authenticate(self, email: str, password: str) -> str | None:
        raise NotImplementedError


class AuthRegister(Protocol):
    @abstractmethod
    async def register(self, email: str, password: str) -> str:
        raise NotImplementedError
