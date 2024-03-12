
from adaptix import Retort, name_mapping
from httpx import AsyncClient
from sqlalchemy import Table, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from costy.adapters.bankapi.bank_gateway import BankGateway
from costy.application.common.bankapi.bankapi_gateway import (
    BankAPIBanksReader,
    BankAPIBulkUpdater,
    BankAPIDeleter,
    BankAPIOperationsReader,
    BankAPIReader,
    BankAPISaver,
    BanksAPIReader,
)
from costy.application.common.bankapi.dto import BankOperationDTO
from costy.domain.exceptions.base import InvalidRequestError
from costy.domain.models.bankapi import BankAPI, BankApiId
from costy.domain.models.user import UserId


class BankAPIGateway(
    BankAPISaver,
    BankAPIDeleter,
    BankAPIBanksReader,
    BankAPIReader,
    BanksAPIReader,
    BankAPIBulkUpdater,
    BankAPIOperationsReader
):
    def __init__(
        self,
        db_session: AsyncSession,
        web_session: AsyncClient,
        table: Table,
        retort: Retort,
        bank_gateways: dict[str, BankGateway],
        banks_info: dict[str, dict]
    ) -> None:
        self._db_session = db_session
        self._web_session = web_session
        self._table = table
        self._retort = retort
        self._bank_gateways = bank_gateways
        self._banks_info = banks_info

    async def get_bankapi(self, bankapi_id: BankApiId) -> BankAPI | None:
        stmt = select(self._table).where(self._table.c.id == bankapi_id)
        result = (await self._db_session.execute(stmt)).mappings()
        return self._retort.load(result, BankAPI)

    async def save_bankapi(self, bankapi: BankAPI) -> None:
        retort = self._retort.extend(recipe=[name_mapping(BankAPI, skip=['id'])])
        values = retort.dump(bankapi)
        query = insert(self._table).values(**values)
        result = await self._db_session.execute(query)
        bankapi.id = result.inserted_primary_key[0]

    async def delete_bankapi(self, bankapi_id: BankApiId) -> None:
        query = delete(self._table).where(self._table.c.id == bankapi_id)
        await self._db_session.execute(query)

    async def get_supported_banks(self) -> tuple[str, ...]:
        return tuple(self._banks_info.keys())

    async def get_bank_access_data_template(self, bank_name: str) -> tuple[str, ...]:
        try:
            return tuple(self._banks_info[bank_name].keys())
        except KeyError:
            raise InvalidRequestError("Invalid data template bank name")

    async def get_bankapi_list(self, user_id: UserId) -> list[BankAPI]:
        stmt = select(self._table).where(self._table.c.user_id == user_id)
        result = (await self._db_session.execute(stmt)).mappings()
        return self._retort.load(result, list[BankAPI])

    async def update_bankapis(self, bankapis: list[BankAPI]) -> None:
        stmts = (
            update(self._table)
            .where(self._table.c.id == bankapi.id)
            .values(updated_at=bankapi.updated_at) for bankapi in bankapis
        )
        for stmt in stmts:
            await self._db_session.execute(stmt)

    async def read_bank_operations(self, bankapi: BankAPI) -> list[BankOperationDTO]:
        bank_gateway = self._bank_gateways[bankapi.name]
        return await bank_gateway.fetch_operations(bankapi.access_data, bankapi.user_id)
