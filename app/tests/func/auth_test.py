"""
Functional account tests
"""
import pytest
from httpx import AsyncClient

from app.tests.config import client_db, database, event_loop  # noqa: F401;


@pytest.mark.asyncio
async def test_auth_token(client_db: AsyncClient):  # noqa: F811;
    """
    Тест app.views.account.login_for_access_token
    Функція повинна вернути JWT, якщо введені дані користувача вірні.
    Якщо ні, то повернути помилку 401.
    """
    user_json = {"email": "test", "password": "test"}  # nosec B106
    await client_db.post("/users/create/", json=user_json)

    auth_json = {"username": user_json["email"], "password": user_json["password"]}
    auth_result = await client_db.post("/token/", data=auth_json)
    assert auth_result.status_code == 200

    result_json = auth_result.json()
    assert all(key in result_json for key in ["access_token", "token_type"])

    incorrect_auth = await client_db.post(
        "/token/", data={"username": "incorrect", "password": "incorrect"}  # nosec B106
    )
    assert incorrect_auth.status_code == 401
