from typing import Any

from litestar.exceptions import HTTPException

from costy.adapters.auth.id_provider import SimpleIdProvider
from costy.application.common.id_provider import IdProvider
from costy.domain.models.user import UserId


async def get_id_provider(cookies: dict[str, Any]) -> IdProvider:
    # This is a simple version that will be improved
    user_id: str | None = cookies.get("user_id")
    if not user_id:
        raise HTTPException("Not authenticated", status_code=401)
    if not user_id.isdigit():
        raise HTTPException("Not valid user_id", status_code=401)
    return SimpleIdProvider(UserId(int(cookies["user_id"])))
