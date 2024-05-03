from costy.application.common.bankapi.bankapi_gateway import BanksAPIReader
from costy.application.common.id_provider import IdProvider
from costy.application.common.interactor import Interactor
from costy.domain.models.bankapi import BankAPI


class ReadBankapiList(Interactor[None, list[BankAPI]]):
    def __init__(
        self,
        bankapi_gateway: BanksAPIReader,
        id_provider: IdProvider,
    ):
        self._bankapi_gateway = bankapi_gateway
        self._id_provider = id_provider

    async def __call__(self, data: None = None) -> list[BankAPI]:
        user_id = await self._id_provider.get_current_user_id()
        return await self._bankapi_gateway.get_bankapi_list(user_id)
