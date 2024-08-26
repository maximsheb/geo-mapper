import logging

from app.settings.base import AppSettings
from app.settings.base import BASE_DIR


class TestAppSettings(AppSettings):
    """
    Application settings class for test environment.
    """

    class Config:
        validate_assigment = True
        env_file = BASE_DIR / ".env.test"

    DEBUG: bool = True
    LOGGING_LEVEL: int = logging.DEBUG
