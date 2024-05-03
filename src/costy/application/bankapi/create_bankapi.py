from typing import Protocol

from ...domain.exceptions.base import InvalidRequestError
from ...domain.services.bankapi import BankAPIService
from ..common.bankapi.bankapi_gateway import BankAPIBanksReader, BankAPISaver
from ..common.bankapi.dto import CreateBankApiDTO
from ..common.id_provider import IdProvider
from ..common.interactor import Interactor
from ..common.uow import UoW


class BankAPIGateway(BankAPIBanksReader, BankAPISaver, Protocol):
    pass


class CreateBankAPI(Interactor[CreateBankApiDTO, None]):
    def __init__(
        self,
        bankapi_service: BankAPIService,
        bankapi_gateway: BankAPIGateway,
        id_provider: IdProvider,
        uow: UoW,
    ) -> None:
        self.bankapi_service = bankapi_service
        self.bankapi_gateway = bankapi_gateway
        self.id_provider = id_provider
        self.uow = uow

    async def __call__(self, data: CreateBankApiDTO) -> None:
        user_id = await self.id_provider.get_current_user_id()
        supported_banks = await self.bankapi_gateway.get_supported_banks()

        if data.name not in supported_banks:
            raise InvalidRequestError("This bank is not supported.")

        access_data_template = await self.bankapi_gateway.get_bank_access_data_template(data.name)
        if tuple(data.access_data) != access_data_template:
            raise InvalidRequestError("Invalid bank access data.")

        bankapi = self.bankapi_service.create(
            data.name,
            data.access_data,
            user_id,
        )

        await self.bankapi_gateway.save_bankapi(bankapi)
        await self.uow.commit()
