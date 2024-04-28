from typing import Type

from litestar import Request, Response

from costy.domain.exceptions.access import AccessDeniedError, AuthenticationError
from costy.domain.exceptions.base import BaseError, InvalidRequestError


def base_error_handler(request: Request, error: BaseError) -> Response:
    errors_detail: dict[Type[BaseError], tuple[str, int]] = {
        AuthenticationError: ("Authentication error", 401),
        AccessDeniedError: ("Access denied error", 403),
        InvalidRequestError: ("Invalid request error", 400),
    }
    detail = errors_detail.get(error.__class__)
    if detail:
        return Response(
            content={
                "error": detail[0],
                "args": error.args,
            },
            status_code=detail[1],
        )
    raise error
