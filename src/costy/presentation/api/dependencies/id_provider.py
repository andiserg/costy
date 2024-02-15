from litestar.exceptions import HTTPException

from costy.adapters.auth.token import TokenIdProvider
from costy.application.common.id_provider import IdProvider


async def get_id_provider(
        headers: dict,
        id_provider_factory: TokenIdProvider
) -> IdProvider:
    if not headers.get("authorization"):
        raise HTTPException("Not authenticated", status_code=401)
    token_type, token = headers.get("authorization", "").split(" ")
    id_provider_factory.token = token
    return id_provider_factory
