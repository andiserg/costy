from typing import Protocol

from costy.application.common.bankapi_gateway import BankAPIDeleter, BankAPIReader
from costy.application.common.commiter import Commiter
from costy.application.common.id_provider import IdProvider
from costy.application.common.interactor import Interactor
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
        commiter: Commiter,
    ) -> None:
        self.access_service = access_service
        self.bankapi_gateway = bankapi_gateway
        self.id_provider = id_provider
        self.commiter = commiter

    async def __call__(self, bankapi_id: BankApiId) -> None:
        user_id = await self.id_provider.get_current_user_id()
        bankapi = await self.bankapi_gateway.get_bankapi(bankapi_id)

        if not bankapi:
            raise InvalidRequestError("Invalid bankapi id.")

        if not self.access_service.ensure_can_edit(bankapi, user_id):
            raise AccessDeniedError(
                "User does not have permission to delete this bankapi.",
            )

        await self.bankapi_gateway.delete_bankapi(bankapi_id)
        await self.commiter.commit()
