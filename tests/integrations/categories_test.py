import pytest
from httpx import AsyncClient

from src.app.services.categories import create_category
from src.app.services.uow.sqlalchemy import SqlAlchemyUnitOfWork
from src.database import Database
from src.schemas.categories import CategoryCreateSchema
from tests.patterns import create_and_auth_func_user


@pytest.mark.asyncio
async def test_create_category_endpoint(client_db: AsyncClient):
    auth_data = await create_and_auth_func_user(client_db)
    token = auth_data["token"]
    headers = {"Authorization": token}

    category_data = {"name": "category name", "icon_name": "", "icon_color": ""}
    response = await client_db.post("/categories/", json=category_data, headers=headers)
    assert response.status_code == 201

    created_category = response.json()
    assert created_category["name"] == category_data["name"]


@pytest.mark.asyncio
async def test_read_categories_endpoint(database: Database, client_db: AsyncClient):
    auth_data = await create_and_auth_func_user(client_db)
    token = auth_data["token"]
    user_id = auth_data["user"]["id"]
    headers = {"Authorization": token}

    async with database.sessionmaker() as session:
        uow = SqlAlchemyUnitOfWork(session)
        for i in range(10):
            schema = CategoryCreateSchema(
                name=f"test category #{i}", icon_name="", icon_color=""
            )
            await create_category(uow, user_id, schema)

    response = await client_db.get("/categories/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 10
