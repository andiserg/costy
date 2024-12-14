import pytest
from litestar.testing import AsyncTestClient
from sqlalchemy import select

from costy.domain.models.bankapi import BankAPI
from costy.infrastructure.db import tables


@pytest.mark.asyncio()
async def test_create_bankapi(app, db_session, db_tables, clean_up_db):
    async with AsyncTestClient(app) as client:
        headers = {"user_id": "1"}
        data = {
            "name": "monobank",
            "access_data": {"X-Token": "aboba"},
        }
        result = await client.post("/bankapi", json=data, headers=headers)

        assert result.status_code == 201


@pytest.mark.asyncio()
async def test_delete_bankapi(app, db_session, db_tables, clean_up_db, bankapi_gateway):
    bankapi = BankAPI(
        user_id=1,
        name="monobank",
        access_data={"X-Token": "aboba"},
    )

    await bankapi_gateway.save_bankapi(bankapi)
    await db_session.commit()

    async with AsyncTestClient(app) as client:
        headers = {"user_id": "1"}

        result = await client.delete(f"/bankapi/{bankapi.id}", headers=headers)

        assert result.status_code == 204

    stmt = select(tables.bankapis).where(tables.bankapis.c.id == bankapi.id)
    result = list(await db_session.execute(stmt))

    assert result == []
