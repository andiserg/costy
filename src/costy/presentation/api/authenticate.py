from litestar import Controller, Response, post
from litestar.datastructures import Cookie

from costy.application.authenticate import LoginInputDTO
from costy.presentation.interactor_factory import InteractorFactory


class AuthenticationController(Controller):
    path = "/auth"

    @post()
    async def login(self, ioc: InteractorFactory, data: LoginInputDTO) -> Response:
        async with ioc.authenticate() as authenticate:
            user_id = await authenticate(data)
        return Response("ok", cookies=[Cookie(key="user_id", value=str(user_id))])
