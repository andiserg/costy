from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, Response, post

from costy.application.authenticate import InputData, Authenticate


class AuthenticationController(Controller):
    path = "/auth"
    tags = ("Authentication",)

    @post(status_code=200)
    @inject
    async def login(
        self,
        authenticate: FromDishka[Authenticate],
        data: InputData,
    ) -> Response[dict[str, str]]:
        token = await authenticate(data)
        if token:
            return Response({"token": token}, status_code=200)
        return Response({"error": "Text"}, status_code=400)
