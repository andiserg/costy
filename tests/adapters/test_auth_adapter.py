import pytest

from costy.application.common.auth_gateway import AuthLoger


@pytest.mark.asyncio()
async def test_authenticate(auth_adapter: AuthLoger, credentials: dict[str, str]):
    token = await auth_adapter.authenticate(credentials["username"], credentials["password"])
    assert isinstance(token, str)
