from fastapi import FastAPI

from fastapi_async_sqlalchemy import SQLAlchemyMiddleware

from app.api.router import api_router
from app.settings import app_config


def create_app() -> FastAPI:
    """
    Create FastAPI application.
    :return: FastAPI application.
    """
    _app = FastAPI(**app_config.fastapi_kwargs)
    _app.include_router(api_router)

    _app.add_middleware(
        SQLAlchemyMiddleware,
        db_url=app_config.SQLALCHEMY_DATABASE_URI,
        engine_args={"echo": False},
    )

    return _app


app: FastAPI = create_app()
