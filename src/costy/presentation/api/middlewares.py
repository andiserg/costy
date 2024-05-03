from litestar.middleware import MiddlewareProtocol
from litestar.types import ASGIApp, Receive, Scope, Send

from costy.infrastructure.metrics import Metrics


def create_metrics_middleware(metrics: Metrics) -> type[MiddlewareProtocol]:
    class MetricsMiddleware(MiddlewareProtocol):
        def __init__(self, app: "ASGIApp") -> None:
            self.app = app

        async def __call__(self, scope: "Scope", receive: "Receive", send: "Send") -> None:
            metrics.total_requests.inc(1)
            await self.app(scope, receive, send)

    return MetricsMiddleware
