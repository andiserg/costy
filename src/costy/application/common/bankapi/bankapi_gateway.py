from abc import abstractmethod
from typing import Protocol, runtime_checkable

from costy.application.common.bankapi.dto import BankOperationDTO
from costy.domain.models.bankapi import BankAPI, BankApiId
from costy.domain.models.user import UserId


@runtime_checkable
class BankAPISaver(Protocol):
    @abstractmethod
    async def save_bankapi(self, bankapi: BankAPI) -> None:
        raise NotImplementedError


@runtime_checkable
class BankAPIOperationsReader(Protocol):
    @abstractmethod
    async def read_bank_operations(self, bankapi: BankAPI) -> list[BankOperationDTO]:
        raise NotImplementedError


@runtime_checkable
class BankAPIDeleter(Protocol):
    @abstractmethod
    async def delete_bankapi(self, bankapi_id: BankApiId) -> None:
        raise NotImplementedError


@runtime_checkable
class BankAPIReader(Protocol):
    @abstractmethod
    async def get_bankapi(self, bankapi_id: BankApiId) -> BankAPI | None:
        raise NotImplementedError


@runtime_checkable
class BanksAPIReader(Protocol):
    @abstractmethod
    async def get_bankapi_list(self, user_id: UserId) -> list[BankAPI]:
        raise NotImplementedError


@runtime_checkable
class BankAPIBanksReader(Protocol):
    @abstractmethod
    async def get_supported_banks(self) -> tuple[str, ...]:
        raise NotImplementedError

    @abstractmethod
    async def get_bank_access_data_template(self, bank_name: str) -> tuple[str, ...]:
        raise NotImplementedError


@runtime_checkable
class BankAPIBulkUpdater(Protocol):
    @abstractmethod
    async def update_bankapis(self, bankapis: list[BankAPI]) -> None:
        raise NotImplementedError
