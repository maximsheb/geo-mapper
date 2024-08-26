import logging

from app.settings.base import AppSettings
from app.settings.base import BASE_DIR


class LocalAppSettings(AppSettings):
    """
    Application settings class for local environment.
    """

    class Config:
        validate_assigment = True
        env_file = BASE_DIR / ".env.local"

    DEBUG: bool = True
    LOGGING_LEVEL: int = logging.DEBUG
