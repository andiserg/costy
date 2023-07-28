from fastapi import FastAPI

from src.database import DatabaseFactory, bind_database_to_app
from src.middlewares import set_cors_middleware


def bootstrap_fastapi_app(db_factory=DatabaseFactory(), test=False) -> FastAPI:
    """
    Setting up FastAPI for operation.
    The setup includes connecting routers, middlewares, and the database.
    """
    fastapi_app = FastAPI()
    include_routers(fastapi_app)
    set_cors_middleware(fastapi_app)
    database = db_factory.get_database(test=test)
    bind_database_to_app(fastapi_app, database)
    # Binding a dependency that provides the database session
    return fastapi_app


def include_routers(fastapi_app):
    """Router connections"""
    from src.routers.auth import router as auth_router  # noqa: E402;
    from src.routers.bank_api import router as bankapi_router  # noqa: E402;
    from src.routers.categories import router as categories_router  # noqa: E402;
    from src.routers.operations import router as operations_router  # noqa: E402;
    from src.routers.statistic import router as statistic_router  # noqa: E402;
    from src.routers.users import router as users_router  # noqa: E402;

    fastapi_app.include_router(users_router, tags=["users"])
    fastapi_app.include_router(auth_router, tags=["account"])
    fastapi_app.include_router(operations_router, tags=["operations"])
    fastapi_app.include_router(bankapi_router, tags=["bankapi"])
    fastapi_app.include_router(statistic_router, tags=["statistic"])
    fastapi_app.include_router(categories_router, tags=["categories"])


app = bootstrap_fastapi_app()
