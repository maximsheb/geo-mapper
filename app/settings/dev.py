import logging

from app.settings.base import AppSettings
from app.settings.base import BASE_DIR


class DevAppSettings(AppSettings):
    """
    Application settings class for docker environment.
    """

    class Config:
        validate_assigment = True
        env_file = BASE_DIR / ".env"

    DEBUG: bool = True
    LOGGING_LEVEL: int = logging.DEBUG
