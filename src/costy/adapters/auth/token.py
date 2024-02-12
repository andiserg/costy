from datetime import datetime, timedelta
from typing import Literal

from aiohttp import ClientSession
from jose import jwt

from costy.application.common.id_provider import IdProvider
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

    def _fetch_rsa_key(self, jwks: dict, unverified_header: dict) -> dict:
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

    def validate_token(self, token: str, jwks: dict) -> UserId:
        invalid_header_error = AuthenticationError(
            {"detail": "Invalid header. Use an RS256 signed JWT Access Token"}
        )
        try:
            unverified_header = jwt.get_unverified_header(token)
        except jwt.JWTError:
            raise invalid_header_error
        if unverified_header["alg"] == "HS256":
            raise invalid_header_error
        rsa_key = self._fetch_rsa_key(jwks, unverified_header)
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=[self.algorithm],
                audience=self.audience,
                issuer=self.issuer
            )
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise AuthenticationError({"detail": "token is expired"})
        except jwt.JWTClaimsError:
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
        self.last_updated = None
        self.uri = uri

    async def get_key_set(self):
        if not self.jwks:
            await self._request_new_key_set()
        return self.jwks

    async def _request_new_key_set(self):
        async with self.session.get(self.uri) as response:
            self.jwks = await response.json()
            self.last_updated = datetime.now()


class TokenIdProvider(IdProvider):
    def __init__(
            self,
            token: str,
            token_processor: JwtTokenProcessor,
            key_set_provider: KeySetProvider,
    ):
        self.token_processor = token_processor
        self.key_set_provider = key_set_provider
        self.token = token

    async def get_current_user_id(self) -> UserId:
        jwks = await self.key_set_provider.get_key_set()
        return self.token_processor.validate_token(self.token, jwks)
