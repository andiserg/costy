from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, delete, get, post

from costy.application.bankapi.create_bankapi import CreateBankAPI
from costy.application.bankapi.delete_bankapi import DeleteBankAPI
from costy.application.bankapi.read_bankapi_list import ReadBankapiList
from costy.application.bankapi.update_bank_operations import UpdateBankOperations
from costy.application.common.bankapi.dto import CreateBankApiDTO
from costy.domain.models.bankapi import BankAPI, BankApiId


class BankAPIController(Controller):
    path = "bankapi"
    tags = ("Banks integration",)

    @get()
    @inject
    async def get_bankapi_list(
        self,
        read_bankapi_list: FromDishka[ReadBankapiList]
    ) -> list[BankAPI]:
        return await read_bankapi_list()

    @post()
    @inject
    async def create_bankapi(
        self,
        create_bankapi: FromDishka[CreateBankAPI],
        data: CreateBankApiDTO,
    ) -> None:
        return await create_bankapi(data)

    @delete("{bankapi_id:int}")
    @inject
    async def delete_bankapi(
        self,
        delete_bankapi: FromDishka[DeleteBankAPI],
        bankapi_id: int,
    ) -> None:
        return await delete_bankapi(BankApiId(bankapi_id))

    @post("/operations")
    @inject
    async def update_bank_operations(
        self,
        update_bank_operations: FromDishka[UpdateBankOperations]
    ) -> None:
        return await update_bank_operations()
