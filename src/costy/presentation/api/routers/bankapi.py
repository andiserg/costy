from litestar import Controller, delete, get, post

from costy.application.common.bankapi.dto import CreateBankApiDTO
from costy.application.common.id_provider import IdProvider
from costy.domain.models.bankapi import BankAPI, BankApiId
from costy.presentation.interactor_factory import InteractorFactory


class BankAPIController(Controller):
    path = "bankapi"
    tags = ("Banks integration",)

    @get()
    async def get_bankapi_list(
        self,
        ioc: InteractorFactory,
        id_provider: IdProvider,
    ) -> list[BankAPI]:
        async with ioc.read_bankapi_list(id_provider) as read_bankapi_list:
            return await read_bankapi_list()

    @post()
    async def create_bankapi(
        self,
        ioc: InteractorFactory,
        id_provider: IdProvider,
        data: CreateBankApiDTO,
    ) -> None:
        async with ioc.create_bankapi(id_provider) as create_bankapi:
            return await create_bankapi(data)

    @delete("{bankapi_id:int}")
    async def delete_bankapi(
        self,
        ioc: InteractorFactory,
        id_provider: IdProvider,
        bankapi_id: int,
    ) -> None:
        async with ioc.delete_bankapi(id_provider) as delete_bankapi:
            return await delete_bankapi(BankApiId(bankapi_id))

    @post("/operations")
    async def update_bank_operations(
        self,
        ioc: InteractorFactory,
        id_provider: IdProvider,
    ) -> None:
        async with ioc.update_bank_operations(id_provider) as update_bank_operations:
            return await update_bank_operations()
