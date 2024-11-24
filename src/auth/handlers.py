from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, Response, post

from auth.application import authenticate, create_user, get_user
from auth.models import UserId


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

    @post()
    @inject
    async def register(
        self,
        service: FromDishka[create_user.CreateUser],
        data: create_user.InputData,
    ) -> dict[str, UserId]:
        user_id = await service(data)
        return {"user_id": user_id}


    @post()
    @inject
    async def get_user(self, headers: dict, service: FromDishka[get_user.GetUser]):
        token = headers.get("Authorization")
        if token:
            user = await service(get_user.InputData(token))
            return {"user_id": user.id}
        return Response(content={"error": "Token is missing"}, status_code=401)
