import pytest
from litestar.testing import AsyncTestClient
from sqlalchemy import select

from costy.domain.models.bankapi import BankAPI
from tests.common.database import create_user


@pytest.mark.asyncio()
async def test_create_bankapi(app, db_session, db_tables, auth_sub, clean_up_db):
    await create_user(db_session, db_tables["users"], auth_sub)

    async with AsyncTestClient(app) as client:
        headers = {"Authorization": "Bearer aboba"}
        data = {
            "name": "monobank",
            "access_data": {"X-Token": "aboba"},
        }
        result = await client.post("/bankapi", json=data, headers=headers)

        assert result.status_code == 201


@pytest.mark.asyncio()
async def test_delete_bankapi(app, db_session, db_tables, auth_sub, clean_up_db, bankapi_gateway):
    user_id = await create_user(db_session, db_tables["users"], auth_sub)

    bankapi = BankAPI(
        user_id=user_id,
        name="monobank",
        access_data={"X-Token": "aboba"},
    )

    await bankapi_gateway.save_bankapi(bankapi)
    await db_session.commit()

    async with AsyncTestClient(app) as client:
        headers = {"Authorization": "Bearer aboba"}

        result = await client.delete(f"/bankapi/{bankapi.id}", headers=headers)

        assert result.status_code == 204

    stmt = select(db_tables["bankapis"]).where(db_tables["bankapis"].c.id == bankapi.id)
    result = list(await db_session.execute(stmt))

    assert result == []
