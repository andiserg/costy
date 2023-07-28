import pytest
from httpx import AsyncClient

from src.app.domain.bank_api import BankInfo, BankInfoProperty
from src.app.services.bank_api import get_bank_managers_by_user, update_banks_costs
from src.app.services.uow.abstract import AbstractUnitOfWork
from src.app.services.uow.sqlalchemy import SqlAlchemyUnitOfWork
from src.database import Database
from tests.patterns import create_and_auth_func_user, create_user_with_orm


async def create_monobank_manager(uow: AbstractUnitOfWork, user_id: int):
    bank_info = BankInfo(bank_name="monobank", user_id=user_id)
    async with uow:
        await uow.banks_info.add(bank_info)
        await uow.banks_info.add(
            BankInfoProperty(
                prop_name="X-Token",
                prop_value="uZFOvRJNeXoVHYTUA_8NgHneWUz8IsG8dRPUbx60mbM4",
                prop_type="str",
                manager=bank_info,
            )
        )
        await uow.commit()


@pytest.mark.asyncio
async def test_update_costs_with_banks(database: Database):
    async with database.sessionmaker() as session:
        # КРОК 1: Створення менеджерів
        uow = SqlAlchemyUnitOfWork(session)
        user = await create_user_with_orm(session)
        await create_monobank_manager(uow, user_id=user.id)

        # КРОК 2: Запис в базу даних витрат за допомогою менеджерів
        managers = await get_bank_managers_by_user(uow, user_id=user.id)
        await update_banks_costs(uow, managers)

    assert True
    # Якщо не виникло помилки - тест пройдений


@pytest.mark.asyncio
async def test_update_costs_with_endpoint(client_db: AsyncClient, database: Database):
    auth_data = await create_and_auth_func_user(client_db)
    token = auth_data["token"]
    user_id = auth_data["user"]["id"]
    headers = {"Authorization": token}
    async with database.sessionmaker() as session:
        # Створення менеджера
        uow = SqlAlchemyUnitOfWork(session)
        await create_monobank_manager(uow, user_id)
    response = await client_db.put("/bankapi/costs/", headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_add_bank_info_with_endpoint(client_db: AsyncClient):
    auth_data = await create_and_auth_func_user(client_db)
    token = auth_data["token"]
    headers = {"Authorization": token}

    response = await client_db.post(
        "/bankapi/",
        json={
            "bank_name": "monobank",
            "X-Token": "uZFOvRJNeXoVHYTUA_8NgHneWUz8IsG8dRPUbx60mbM4",
        },
        headers=headers,
    )
    assert response.status_code == 201
