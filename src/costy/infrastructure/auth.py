from datetime import timedelta
from typing import Any, Callable, Coroutine

from aiohttp import ClientSession

from costy.adapters.auth.token import (
    Algorithm,
    JwtTokenProcessor,
    KeySetProvider,
    TokenIdProvider,
)


def create_id_provider_factory(
        audience: str,
        algorithm: Algorithm,
        issuer: str,
        jwsk_uri: str,
        web_session: ClientSession,
        jwsk_expired: timedelta = timedelta(days=1)
) -> Callable[[], Coroutine[Any, Any, TokenIdProvider]]:
    token_processor = JwtTokenProcessor(algorithm, audience, issuer)
    jwsk_provider = KeySetProvider(jwsk_uri, web_session, jwsk_expired)

    async def factory() -> TokenIdProvider:
        return TokenIdProvider(token_processor, jwsk_provider)

    return factory
