from typing import Protocol

from ...domain.models.operation import Operation
from ...domain.services.bankapi import BankAPIService
from ...domain.services.operation import OperationService
from ..common.bankapi.bankapi_gateway import BankAPIBulkUpdater, BankAPIOperationsReader, BanksAPIReader
from ..common.category.category_gateway import CategoriesFinder, CategoryFinder
from ..common.id_provider import IdProvider
from ..common.interactor import Interactor
from ..common.operation.operation_gateway import OperationsBulkSaver
from ..common.uow import UoW


class BankAPIGateway(BankAPIBulkUpdater, BanksAPIReader, BankAPIOperationsReader, Protocol):
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
        uow: UoW,
    ):
        self._bankapi_service = bankapi_service
        self._operation_service = operation_service
        self._bankapi_gateway = bankapi_gateway
        self._operation_gateway = operation_gateway
        self._category_gateway = category_gateway
        self._id_provider = id_provider
        self._uow = uow

    async def __call__(self, data=None) -> None:
        user_id = await self._id_provider.get_current_user_id()
        bankapis = await self._bankapi_gateway.get_bankapi_list(user_id)
        default_category = await self._category_gateway.find_category(name="Інше", kind="general")

        operations: list[Operation] = []
        for bankapi in bankapis:
            bank_operations = await self._bankapi_gateway.read_bank_operations(bankapi)
            mcc_codes = tuple(operation.mcc for operation in bank_operations)
            mcc_categories = await self._category_gateway.find_categories_by_mcc_codes(mcc_codes)

            for bank_operation in bank_operations:
                category = mcc_categories.get(bank_operation.mcc, default_category)
                if category:
                    self._operation_service.set_category(bank_operation.operation, category)

            operations.extend(bank_operation.operation for bank_operation in bank_operations)
            self._bankapi_service.update_time(bankapi)

        if operations:
            await self._operation_gateway.save_operations(operations)

        await self._bankapi_gateway.update_bankapis(bankapis)
        await self._uow.commit()
