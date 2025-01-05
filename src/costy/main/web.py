import asyncio
from typing import Any

from dishka import make_async_container
from dishka.integrations.litestar import setup_dishka
from httpx import AsyncClient
from litestar import Litestar
from litestar.config.cors import CORSConfig
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from costy.domain.exceptions.base import BaseError
from costy.infrastructure.config import (
    get_banks_conf,
    get_db_connection_url,
    setup_logger,
)
from costy.infrastructure.db.main import get_engine, get_sessionmaker
from costy.infrastructure.metrics import create_metrics, start_metrics_server
from costy.main.di import DIProvider, IdDIProvider
from costy.presentation.api.exception_handlers import base_error_handler
from costy.presentation.api.middlewares import create_metrics_middleware
from costy.presentation.api.routers.bankapi import BankAPIController
from costy.presentation.api.routers.category import CategoryController
from costy.presentation.api.routers.operation import OperationController


def init_app() -> Litestar:
    setup_logger()

    web_session = AsyncClient()
    metrics = create_metrics()

    container = make_async_container(
        DIProvider(),
        IdDIProvider(),
        context={
            AsyncClient: web_session,
            async_sessionmaker[AsyncSession]: get_sessionmaker(
                get_engine(get_db_connection_url()),
            ),
            dict[str, dict[str, Any]]: get_banks_conf(),
        },
    )

    async def startup() -> None:
        await asyncio.create_task(asyncio.to_thread(start_metrics_server))

    async def finalization() -> None:
        await web_session.aclose()

    app = Litestar(
        route_handlers=(
            OperationController,
            CategoryController,
            BankAPIController,
        ),
        path="/api",
        on_shutdown=[finalization],
        on_startup=[startup],
        exception_handlers={BaseError: base_error_handler},
        middleware=[create_metrics_middleware(metrics)],
        debug=True,
        cors_config=CORSConfig(allow_origins=["*"]),
    )
    setup_dishka(container, app)
    return app
