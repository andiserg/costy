from datetime import UTC, datetime
from typing import Any

from adaptix import Retort, name_mapping
from httpx import AsyncClient
from sqlalchemy import Table, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from costy.adapters.bankapi.bank_gateway import BankAdapter
from costy.adapters.db.category_gateway import CategoryAdapter
from costy.application.common.bankapi_gateway import (
    BankAPIBanksReader,
    BankAPIBulkUpdater,
    BankAPIDeleter,
    BankAPIOperationsReader,
    BankAPIReader,
    BankAPISaver,
    BanksAPIReader,
    Operation,
)
from costy.domain.exceptions.base import InvalidRequestError
from costy.domain.models.bankapi import BankAPI, BankApiId
from costy.domain.models.user import UserId

retort = Retort()
modified_retort = retort.extend(recipe=[name_mapping(BankAPI, skip=["id"])])


class BankAPIAdapter(
    BankAPISaver,
    BankAPIDeleter,
    BankAPIBanksReader,
    BankAPIReader,
    BanksAPIReader,
    BankAPIBulkUpdater,
    BankAPIOperationsReader,
):
    def __init__(
        self,
        db_session: AsyncSession,
        web_session: AsyncClient,
        table: Table,
        bank_gateways: dict[str, BankAdapter],
        banks_info: dict[str, dict[str, Any]],
        category_adapter: CategoryAdapter
    ) -> None:
        self._db_session = db_session
        self._web_session = web_session
        self._table = table
        self._bank_gateways = bank_gateways
        self._banks_info = banks_info
        self._category_adapter = category_adapter


    async def get_bankapi(self, bankapi_id: BankApiId) -> BankAPI | None:
        stmt = select(self._table).where(self._table.c.id == bankapi_id)
        result = next((await self._db_session.execute(stmt)).mappings(), None)
        return retort.load(result, BankAPI) if result else None

    async def save_bankapi(self, bankapi: BankAPI) -> None:
        values = modified_retort.dump(bankapi)
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
            return tuple(self._banks_info[bank_name]["access_fields"])
        except KeyError:
            raise InvalidRequestError("Invalid data template bank name")

    async def get_bankapi_list(self, user_id: UserId) -> list[BankAPI]:
        stmt = select(self._table).where(self._table.c.user_id == user_id)
        result = (await self._db_session.execute(stmt)).mappings()
        return retort.load(result, list[BankAPI])

    async def update_bankapis(self, bankapis: list[BankAPI]) -> None:
        stmts = (
            update(self._table)
            .where(self._table.c.id == bankapi.id)
            .values(updated_at=bankapi.updated_at)
            for bankapi in bankapis
        )
        for stmt in stmts:
            await self._db_session.execute(stmt)

    async def read_bank_operations(
        self,
        bankapi: BankAPI,
    ) -> tuple[Operation, ...] | None:
        bank_gateway = self._bank_gateways[bankapi.name]
        from_time = (
            datetime.fromtimestamp(bankapi.updated_at, tz=UTC)
            if bankapi.updated_at
            else None
        )
        bank_operations = await bank_gateway.fetch_operations(
            bankapi.access_data,
            bankapi.user_id,
            from_time,
        )
        mcc_codes = tuple(operation.mcc for operation in bank_operations)
        mcc_categories = await self._category_adapter.find_categories_by_mcc_codes(
            mcc_codes,
        )

        default_category = await self._category_adapter.find_category(
            name="Інше",
            kind="general",
        )

        for bank_operation in bank_operations:
            category = mcc_categories.get(bank_operation.mcc, default_category)
            if category:
                bank_operation.operation.category_id = category.id

        return tuple(bank_operation.operation for bank_operation in bank_operations)
