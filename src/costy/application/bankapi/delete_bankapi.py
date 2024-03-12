from typing import Protocol

from costy.application.common.bankapi.bankapi_gateway import (
    BankAPIDeleter,
    BankAPIReader,
)
from costy.application.common.id_provider import IdProvider
from costy.application.common.interactor import Interactor
from costy.application.common.uow import UoW
from costy.domain.exceptions.access import AccessDeniedError
from costy.domain.exceptions.base import InvalidRequestError
from costy.domain.models.bankapi import BankApiId
from costy.domain.services.access import AccessService


class BankAPIGateway(BankAPIReader, BankAPIDeleter, Protocol):
    pass


class DeleteBankAPI(Interactor[BankApiId, None]):
    def __init__(
        self,
        access_service: AccessService,
        bankapi_gateway: BankAPIGateway,
        id_provider: IdProvider,
        uow: UoW
    ):
        self._access_service = access_service
        self._bankapi_gateway = bankapi_gateway
        self._id_provider = id_provider
        self._uow = uow

    async def __call__(self, bankapi_id: BankApiId) -> None:
        user_id = await self._id_provider.get_current_user_id()
        bankapi = await self._bankapi_gateway.get_bankapi(bankapi_id)

        if not bankapi:
            raise InvalidRequestError("Invalid bankapi id.")

        if not self._access_service.ensure_can_edit(bankapi, user_id):
            raise AccessDeniedError("User does not have permission to delete this bankapi.")

        await self._bankapi_gateway.delete_bankapi(bankapi_id)
        await self._uow.commit()
