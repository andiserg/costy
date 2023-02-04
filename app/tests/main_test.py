"""
Testing main.py
"""

import pytest
from httpx import AsyncClient

from app.main import app


@pytest.fixture
def anyio_backend():
    """
    За замовчуванням, async тест обернутий в @pytest.mark.anyio
    намагається виконатись також у trio, альтернативі asyncio, і видає failed тест
    """
    return "asyncio"


@pytest.mark.anyio
async def test_root():
    """
    Тестування app.main.root
    """
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as client:
        response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
