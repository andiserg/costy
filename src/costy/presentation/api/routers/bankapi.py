from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, delete, get, post

from costy.application.bankapi import (
    create_bankapi,
    delete_bankapi,
    read_bankapi_list,
    update_bank_operations,
)
from costy.domain.models.bankapi import BankAPI, BankApiId


class BankAPIController(Controller):
    path = "bankapi"
    tags = ("Banks integration",)

    @get()
    @inject
    async def get_bankapi_list(
        self,
        service: FromDishka[read_bankapi_list.ReadBankapiList],
    ) -> list[BankAPI]:
        return await service()

    @post()
    @inject
    async def create_bankapi(
        self,
        service: FromDishka[create_bankapi.CreateBankAPI],
        data: create_bankapi.InputData,
    ) -> None:
        return await service(data)

    @delete("{bankapi_id:int}")
    @inject
    async def delete_bankapi(
        self,
        service: FromDishka[delete_bankapi.DeleteBankAPI],
        bankapi_id: int,
    ) -> None:
        return await service(BankApiId(bankapi_id))

    @post("/operations")
    @inject
    async def update_bank_operations(
        self,
        service: FromDishka[update_bank_operations.UpdateBankOperations],
    ) -> None:
        return await service(None)
