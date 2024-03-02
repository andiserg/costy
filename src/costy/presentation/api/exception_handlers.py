from litestar import Request, Response

from costy.domain.exceptions.access import (
    AccessDeniedError,
    AuthenticationError,
)


def auth_error_handler(request: Request, error: AuthenticationError) -> Response:
    return Response(
        content={
            "error": "Authentication error",
            "args": error.args
        },
        status_code=401
    )


def access_denied_handler(request: Request, error: AccessDeniedError) -> Response:
    return Response(
        content={
            "error": "Access denied error",
            "args": error.args
        },
        status_code=403
    )
