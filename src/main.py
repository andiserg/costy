"""
Головний файл програми
"""
from fastapi import FastAPI

from src.database import DatabaseFactory, bind_database_to_app
from src.middlewares import set_cors_middleware


def bootstrap_fastapi_app(db_factory=DatabaseFactory(), test=False) -> FastAPI:
    """Налаштування FastApi для початку роботи, включаючи базу"""
    fastapi_app = FastAPI()
    include_routers(fastapi_app)
    set_cors_middleware(fastapi_app)
    database = db_factory.get_database(test=test)
    bind_database_to_app(fastapi_app, database)
    # Прив'язка залежності, яка віддає сесію бази
    return fastapi_app


def include_routers(fastapi_app):
    """Підключення роутерів"""
    from src.routers.auth import router as auth_router  # noqa: E402;
    from src.routers.bank_api import router as bankapi_router  # noqa: E402;
    from src.routers.categories import router as categories_router  # noqa: E402;
    from src.routers.limits import router as limits_router
    from src.routers.operations import router as operations_router  # noqa: E402;
    from src.routers.statistic import router as statistic_router  # noqa: E402;
    from src.routers.users import router as users_router  # noqa: E402;

    fastapi_app.include_router(users_router, tags=["users"])
    fastapi_app.include_router(auth_router, tags=["account"])
    fastapi_app.include_router(operations_router, tags=["operations"])
    fastapi_app.include_router(bankapi_router, tags=["bankapi"])
    fastapi_app.include_router(statistic_router, tags=["statistic"])
    fastapi_app.include_router(categories_router, tags=["categories"])
    fastapi_app.include_router(limits_router, tags=["limits"])


app = bootstrap_fastapi_app()
