from litestar.types import ASGIApp, Receive, Scope, Send


def metrics_middleware_factory(app: ASGIApp) -> ASGIApp:
    async def metrics_middleware(scope: Scope, receive: Receive, send: Send) -> None:
        await app(scope, receive, send)

    return metrics_middleware

