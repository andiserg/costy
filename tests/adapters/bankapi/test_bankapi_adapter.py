import importlib.resources
import json

import pytest
from sqlalchemy import select

from costy.domain.services.bankapi import BankAPIService
from costy.infrastructure.db import tables


@pytest.mark.asyncio()
async def test_save_bankapi(bankapi_gateway, db_session, db_tables):
    bankapi = BankAPIService().create("test", {}, 1)

    await bankapi_gateway.save_bankapi(bankapi)

    assert bankapi.id is not None


@pytest.mark.asyncio()
async def test_delete_bankapi(bankapi_gateway, db_session, db_tables):
    bankapi = BankAPIService().create("test", {}, 1)
    await bankapi_gateway.save_bankapi(bankapi)

    await bankapi_gateway.delete_bankapi(bankapi.id)

    assert list(await db_session.execute(
        select(tables.bankapis)
        .where(tables.bankapis.c.id == bankapi.id),
    )) == []



@pytest.mark.asyncio()
async def test_get_supported_banks(bankapi_gateway):
    with open(str(importlib.resources.files("costy.adapters.bankapi") / "_banks.json"), "r") as f:
        banks = json.load(f)

    assert await bankapi_gateway.get_supported_banks() == tuple(banks.keys())


@pytest.mark.asyncio()
async def test_get_bankapi_list(bankapi_gateway, db_session, db_tables):
    created_bankapis = [
        BankAPIService().create(f"test #{i}", {}, 1)
        for i in range(5)
    ]

    for bankapi in created_bankapis:
        await bankapi_gateway.save_bankapi(bankapi)

    bankapis = await bankapi_gateway.get_bankapi_list(1)

    assert bankapis == created_bankapis


@pytest.mark.asyncio()
async def test_update_bankapis(bankapi_gateway, db_session, db_tables):
    service = BankAPIService()

    created_bankapis = [
        service.create(f"test #{i}", {}, 1)
        for i in range(5)
    ]

    for bankapi in created_bankapis:
        await bankapi_gateway.save_bankapi(bankapi)

    for bankapi in created_bankapis:
        service.update_time(bankapi)
    await bankapi_gateway.update_bankapis(created_bankapis)

    bankapis = await bankapi_gateway.get_bankapi_list(1)

    assert bankapis == created_bankapis


@pytest.mark.asyncio()
async def test_read_bank_operations(bankapi_gateway, user_id):
    bankapi = BankAPIService().create("test_bank", {}, user_id)
    assert await bankapi_gateway.read_bank_operations(bankapi)
