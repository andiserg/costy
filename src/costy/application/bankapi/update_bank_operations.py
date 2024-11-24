from typing import Protocol

from ...domain.models.operation import Operation
from ...domain.services.bankapi import BankAPIService
from ...domain.services.operation import OperationService
from ..common.bankapi_gateway import (
    BankAPIBulkUpdater,
    BankAPIOperationsReader,
    BanksAPIReader,
)
from ..common.category_gateway import CategoriesFinder, CategoryFinder
from ..common.commiter import Commiter
from ..common.id_provider import IdProvider
from ..common.interactor import Interactor
from ..common.operation_gateway import OperationsBulkSaver


class BankAPIGateway(
    BankAPIBulkUpdater,
    BanksAPIReader,
    BankAPIOperationsReader,
    Protocol,
):
    pass


class CategoryGateway(CategoriesFinder, CategoryFinder, Protocol):
    pass


class UpdateBankOperations(Interactor[None, None]):
    def __init__(
        self,
        bankapi_service: BankAPIService,
        operation_service: OperationService,
        bankapi_gateway: BankAPIGateway,
        operation_gateway: OperationsBulkSaver,
        category_gateway: CategoryGateway,
        id_provider: IdProvider,
        uow: Commiter,
    ) -> None:
        self.bankapi_service = bankapi_service
        self.operation_service = operation_service
        self.bankapi_gateway = bankapi_gateway
        self.operation_gateway = operation_gateway
        self.category_gateway = category_gateway
        self.id_provider = id_provider
        self.commiter = uow

    async def __call__(self, data: None) -> None:
        user_id = await self.id_provider.get_current_user_id()
        bankapis = await self.bankapi_gateway.get_bankapi_list(user_id)

        operations: list[Operation] = []
        for bankapi in bankapis:
            operations.extend(await self.bankapi_gateway.read_bank_operations(bankapi))
            self.bankapi_service.update_time(bankapi)

        if operations:
            await self.operation_gateway.save_operations(operations)

        await self.bankapi_gateway.update_bankapis(bankapis)
        await self.commiter.commit()
