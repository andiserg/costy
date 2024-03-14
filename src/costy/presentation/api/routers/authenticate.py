from litestar import Controller, Response, post

from costy.application.authenticate import LoginInputDTO
from costy.presentation.interactor_factory import InteractorFactory


class AuthenticationController(Controller):
    path = "/auth"
    tags = ("Authentication",)

    @post(status_code=200)
    async def login(self, ioc: InteractorFactory, data: LoginInputDTO) -> Response[dict[str, str]]:
        async with ioc.authenticate() as authenticate:
            token = await authenticate(data)
            if token:
                return Response({"token": token}, status_code=200)
            return Response({"error": "Text"}, status_code=400)
