from datetime import datetime, timedelta
from typing import Any, Literal

from aiohttp import ClientSession
from jose import exceptions as jwt_exc
from jose import jwt

from costy.application.common.id_provider import IdProvider
from costy.application.common.user_gateway import UserReader
from costy.domain.exceptions.access import AuthenticationError
from costy.domain.models.user import UserId

Algorithm = Literal[
    "HS256", "HS384", "HS512",
    "RS256", "RS384", "RS512",
]


class JwtTokenProcessor:
    def __init__(
            self,
            algorithm: Algorithm,
            audience: str,
            issuer: str,
    ):
        self.algorithm = algorithm
        self.audience = audience
        self.issuer = issuer

    def _fetch_rsa_key(self, jwks: dict[Any, Any], unverified_header: dict[str, str]) -> dict[str, str]:
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        return rsa_key

    def validate_token(self, token: str, jwks: dict[Any, Any]) -> str:
        invalid_header_error = AuthenticationError(
            {"detail": "Invalid header. Use an RS256 signed JWT Access Token"}
        )
        try:
            unverified_header = jwt.get_unverified_header(token)
        except jwt_exc.JWTError:
            raise invalid_header_error
        if unverified_header["alg"] == "HS256":
            raise invalid_header_error
        rsa_key = self._fetch_rsa_key(jwks, unverified_header)
        try:
            payload: dict[str, str] = jwt.decode(
                token,
                rsa_key,
                algorithms=[self.algorithm],
                audience=self.audience,
                issuer=self.issuer
            )
            return payload["sub"].replace("auth0|", "")
        except jwt_exc.ExpiredSignatureError:
            raise AuthenticationError({"detail": "token is expired"})
        except jwt_exc.JWTClaimsError:
            raise AuthenticationError(
                {"detail": "incorrect claims (check audience and issuer)"}
            )
        except Exception:
            raise AuthenticationError(
                {"detail": "Unable to parse authentication token."}
            )


class KeySetProvider:
    def __init__(self, uri: str, session: ClientSession, expired: timedelta):
        self.session = session
        self.jwks: dict[str, str] = {}
        self.expired = expired
        self.last_updated: datetime | None = None
        self.uri = uri

    async def get_key_set(self) -> dict[Any, Any]:
        if not self.jwks:
            await self._request_new_key_set()
        if self.last_updated and datetime.now() - self.last_updated > self.expired:
            # TODO: add use Cache-Control
            await self._request_new_key_set()
        return self.jwks

    async def _request_new_key_set(self) -> None:
        async with self.session.get(self.uri) as response:
            self.jwks = await response.json()
            self.last_updated = datetime.now()


class TokenIdProvider(IdProvider):
    def __init__(
            self,
            token_processor: JwtTokenProcessor,
            key_set_provider: KeySetProvider,
            token: str | None = None
    ):
        self.token_processor = token_processor
        self.key_set_provider = key_set_provider
        self.token = token
        self.user_gateway: UserReader | None = None

    async def get_current_user_id(self) -> UserId:
        if self.token and self.user_gateway:
            jwks = await self.key_set_provider.get_key_set()
            sub = self.token_processor.validate_token(self.token, jwks)
            user_id = await self.user_gateway.get_user_id_by_auth_id(sub)
            return UserId(user_id)
        raise AuthenticationError()
