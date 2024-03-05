from litestar.exceptions import HTTPException

from costy.application.common.id_provider import IdProvider


async def get_id_provider(
        headers: dict[str, str],
        id_provider_pure: IdProvider
) -> IdProvider:
    if not headers.get("authorization"):
        raise HTTPException("Not authenticated", status_code=401)
    token_type, token = headers.get("authorization", "").split(" ")
    id_provider_pure.token = token  # type: ignore
    return id_provider_pure
