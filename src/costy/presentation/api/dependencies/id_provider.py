from typing import Annotated, Callable

from litestar.exceptions import HTTPException
from litestar.params import Parameter

from costy.application.common.id_provider import IdProvider


async def get_id_provider(
        token: Annotated[str, Parameter(header="Authorization")],
        id_provider_factory: Callable
) -> IdProvider:
    if not token:
        raise HTTPException("Not authenticated", status_code=401)
    token_type, token = token.split(" ")
    return id_provider_factory(token)
