from ..common.bankapi_gateway import BanksAPIReader
from ..common.id_provider import IdProvider
from ..common.interactor import Interactor
from costy.domain.models.bankapi import BankAPI


class ReadBankapiList(Interactor[None, list[BankAPI]]):
    def __init__(
        self,
        bankapi_gateway: BanksAPIReader,
        id_provider: IdProvider,
    ) -> None:
        self.bankapi_gateway = bankapi_gateway
        self.id_provider = id_provider

    async def __call__(self, data: None = None) -> list[BankAPI]:
        user_id = await self.id_provider.get_current_user_id()
        return await self.bankapi_gateway.get_bankapi_list(user_id)
