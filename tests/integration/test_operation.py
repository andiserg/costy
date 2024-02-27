import pytest
from litestar.testing import AsyncTestClient


@pytest.mark.asyncio
async def test_create_operation(app, user_token, create_sub_user, db_category_id):
    async with AsyncTestClient(app) as client:
        headers = {"Authorization": f"Bearer {user_token}"}
        data = {
            "amount": 100,
            "category_id": db_category_id
        }
        result = await client.post("/operations", json=data, headers=headers)

        assert result.status_code == 201
        assert isinstance(result.json(), int)


@pytest.mark.asyncio
async def test_get_list_operations():
    pass
