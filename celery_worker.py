from celery import Celery

from app.settings import app_config

celery_app = Celery(
    "celery-worker",
    broker=app_config.REDIS_URL,
    backend=app_config.REDIS_URL
)

celery_app.conf.update(
    task_serializer="json", result_serializer="json", accept_content=["json"]
)


import app.services.task
