import logging
from datetime import UTC, datetime, timedelta
from typing import Any, Literal

from httpx import AsyncClient
from jose import exceptions as jwt_exc
from jose import jwt

from auth.application._common import UserProvider, UserReader
from auth.exceptions import AuthenticationError
from auth.models import User

Algorithm = Literal[
    "HS256",
    "HS384",
    "HS512",
    "RS256",
    "RS384",
    "RS512",
]

logger = logging.getLogger(__name__)


class JwtTokenProcessor:
    def __init__(
        self,
        algorithm: Algorithm,
        audience: str,
        issuer: str,
    ) -> None:
        self.algorithm = algorithm
        self.audience = audience
        self.issuer = issuer

    def _fetch_rsa_key(
        self,
        jwks: dict[Any, Any],
        unverified_header: dict[str, str],
    ) -> dict[str, str]:
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
        return rsa_key

    def validate_token(self, token: str, jwks: dict[Any, Any]) -> str:
        invalid_header_error = AuthenticationError(
            {"detail": "Invalid header. Use an RS256 signed JWT Access Token"},
        )
        try:
            unverified_header = jwt.get_unverified_header(token)
        except jwt_exc.JWTError:
            raise invalid_header_error
        if unverified_header["alg"] == "HS256":
            logger.info(
                "Token decode error. "
                f"Invalid encode algorithm: {unverified_header['alg']}",
            )
            raise invalid_header_error
        rsa_key = self._fetch_rsa_key(jwks, unverified_header)
        try:
            payload: dict[str, str] = jwt.decode(
                token,
                rsa_key,
                algorithms=[self.algorithm],
                audience=self.audience,
                issuer=self.issuer,
            )
            return payload["sub"].replace("auth0|", "")
        except jwt_exc.ExpiredSignatureError:
            raise AuthenticationError({"detail": "token is expired"})
        except jwt_exc.JWTClaimsError:
            message = "incorrect claims (check audience and issuer)"
            logger.exception("Auth token resolving fail. Message: %s", message)
            raise AuthenticationError(
                {"detail": "incorrect claims (check audience and issuer)"},
            )
        except jwt_exc.JOSEError as e:
            logger.warning("Auth token resolving unknown error. Message: %s", e.args)
            raise AuthenticationError(
                {"detail": "Unable to parse authentication token."},
            ) from e


class KeySetProvider:
    def __init__(self, uri: str, session: AsyncClient, expired: timedelta) -> None:
        self.session = session
        self.jwks: dict[str, str] = {}
        self.expired = expired
        self.last_updated: datetime | None = None
        self.uri = uri

    async def get_key_set(self) -> dict[Any, Any]:
        if not self.jwks:
            await self._request_new_key_set()

        now = datetime.now(tz=UTC)
        if self.last_updated and now - self.last_updated > self.expired:
            # TODO: add use Cache-Control
            await self._request_new_key_set()
        return self.jwks

    async def _request_new_key_set(self) -> None:
        response = await self.session.get(self.uri)
        self.jwks = response.json()
        self.last_updated = datetime.now(tz=UTC)


class TokenUserProvider(UserProvider):
    def __init__(
        self,
        token_processor: JwtTokenProcessor,
        key_set_provider: KeySetProvider,
        user_gateway: UserReader,
    ) -> None:
        self.token_processor = token_processor
        self.key_set_provider = key_set_provider
        self.user_gateway = user_gateway

    async def get_user_by_token(self, token: str) -> User:
        jwks = await self.key_set_provider.get_key_set()
        sub = self.token_processor.validate_token(token, jwks)
        return await self.user_gateway.get_user_by_auth_id(sub)
