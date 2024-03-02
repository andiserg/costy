from costy.domain.exceptions.base import BaseError


class AuthenticationError(BaseError):
    pass


class RegisterError(BaseError):
    pass


class AccessDeniedError(BaseError):
    pass
