from app.settings.base import AppSettings
from app.settings.local import LocalAppSettings
from app.settings.test import TestAppSettings


environments = {
    "local": LocalAppSettings,
    "test": TestAppSettings,
}


def __get_app_settings() -> AppSettings:
    config_class = environments["local"]
    return config_class()


app_config = __get_app_settings()

__all__ = ["app_config"]
