import os

from app.settings.base import AppSettings
from app.settings.dev import DevAppSettings
from app.settings.local import LocalAppSettings
from app.settings.test import TestAppSettings


environments = {
    "local": LocalAppSettings,
    "test": TestAppSettings,
    "dev": DevAppSettings,
}


def __get_app_settings() -> AppSettings:
    config_class = environments[os.getenv("ENV", "local").lower()]
    return config_class()


app_config = __get_app_settings()

__all__ = ["app_config"]
