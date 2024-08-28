import pathlib

from typing import Optional, Any
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings

from sqlalchemy import URL

BASE_DIR = pathlib.Path(__file__).resolve().parents[2]


class AppSettings(BaseSettings):
    """
    Application main settings class.
    """

    class Config:
        validate_assignment = True

    DEBUG: bool = False
    DOCS_URL: str = "/docs"
    OPENAPI_PREFIX: str = ""
    ROOT_PATH: str = ""
    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: str = "/redoc"
    TITLE: str = "Payment API service"
    DESCRIPTION: str = (
        "Service that provides mapping between "
        "geo points with distance resolution"
    )
    VERSION: str = Field(default="unknown", env="VERSION")

    ALLOWED_HOSTS: list[str] = ["*"]

    # Run app environment
    ENV: str = Field(default="local", env="ENV")

    # App run settings
    HOST: str = Field(default="127.0.0.1", env="HOST")
    PORT: int = Field(default=8080, env="PORT")

    # Redis settings
    REDIS_URL: str

    # Database settings
    DB_SERVER: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: str = Field(default="5432", env="DB_PORT")
    SQLALCHEMY_DATABASE_URI: Optional[URL] = None
    DB_CONSOLE_LOGGING: bool = False

    @model_validator(mode="before")
    def assemble_db_connection(cls, values: dict[str, Any]) -> dict[str, Any]:
        if "SQLALCHEMY_DATABASE_URI" in values and isinstance(
            values["SQLALCHEMY_DATABASE_URI"], str
        ):
            return values

        values["SQLALCHEMY_DATABASE_URI"] = URL.create(
            "postgresql+asyncpg",
            username=values.get("DB_USER"),
            password=values.get("DB_PASSWORD"),
            host=values.get("DB_SERVER"),
            port=values.get("DB_PORT"),
            database=values.get("DB_NAME"),
        )
        return values

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        return {
            "debug": self.DEBUG,
            "docs_url": self.DOCS_URL,
            "openapi_prefix": self.OPENAPI_PREFIX,
            "openapi_url": self.OPENAPI_URL,
            "redoc_url": self.REDOC_URL,
            "title": self.TITLE,
            "descriptions": self.DESCRIPTION,
            "version": self.VERSION,
        }
