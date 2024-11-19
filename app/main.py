import uvicorn

from prometheus_fastapi_instrumentator import Instrumentator

from app.settings import app_config
from app.utils.fastapi_app import app

Instrumentator().instrument(app).expose(app)

if __name__ == "__main__":
    uvicorn.run(app, host=app_config.HOST, port=app_config.PORT)
