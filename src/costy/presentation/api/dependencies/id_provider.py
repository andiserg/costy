from litestar.exceptions import HTTPException

from costy.application.common.id_provider import IdProvider


async def get_id_provider(
        headers: dict[str, str],
        id_provider_blank: IdProvider,
) -> IdProvider:
    authorization = headers.get("authorization")
    if not authorization:
        raise HTTPException("Not authenticated", status_code=401)
    token_type, token = authorization.split(" ")
    id_provider_blank.token = token  # type: ignore[attr-defined]
    return id_provider_blank
