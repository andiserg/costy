from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, Request, Response, get, post

from auth.application import authenticate, create_user, get_user
from auth.exceptions import AuthenticationError, BaseError, RegisterError


class AuthenticationController(Controller):
    path = "/auth"
    tags = ("Authentication",)

    @post(status_code=200)
    @inject
    async def login(
        self,
        service: FromDishka[authenticate.Authenticate],
        data: authenticate.InputData,
    ) -> Response[dict[str, str]]:
        token = await service(data)
        if token:
            return Response({"token": token}, status_code=200)
        return Response({"error": "Invalid data"}, status_code=400)


class UserController(Controller):
    path = "/users"
    tags = ("Users",)

    @post(status_code=201)
    @inject
    async def register(
        self,
        service: FromDishka[create_user.CreateUser],
        data: create_user.InputData,
    ) -> None:
        await service(data)
        return None

    @get(status_code=200)
    @inject
    async def get_user(
        self,
        headers: dict[str, str],
        service: FromDishka[get_user.GetUser],
    ) -> dict[str, int | None] | Response:  # type: ignore[type-arg]
        token = headers.get("authorization")
        if token:
            user = await service(get_user.InputData(token))
            return Response("authenticated", headers={"user_id": str(user.id)})
        return Response(content={"error": "Token is missing"}, status_code=401)


def base_error_handler(_: Request, error: BaseError) -> Response:  # type: ignore[type-arg]
    errors_detail: dict[type[BaseError], tuple[str, int]] = {
        AuthenticationError: ("Authentication error", 401),
        RegisterError: ("Register error", 400),
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
