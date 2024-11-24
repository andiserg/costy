from datetime import timedelta
from typing import Any, Callable, Coroutine

from httpx import AsyncClient

from auth.adapters.token import (
    Algorithm,
    JwtTokenProcessor,
    KeySetProvider,
    TokenUserProvider,
)


def create_id_provider_factory(
    audience: str,
    algorithm: Algorithm,
    issuer: str,
    jwsk_uri: str,
    web_session: AsyncClient,
    jwsk_expired: timedelta = timedelta(days=1),
) -> Callable[[], Coroutine[Any, Any, TokenUserProvider]]:
    token_processor = JwtTokenProcessor(algorithm, audience, issuer)
    jwsk_provider = KeySetProvider(jwsk_uri, web_session, jwsk_expired)

    async def factory() -> TokenUserProvider:
        return TokenUserProvider(token_processor, jwsk_provider)

    return factory
