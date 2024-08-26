import uvicorn

from app.settings import app_config
from app.utils.fastapi_app import app


if __name__ == "__main__":
    uvicorn.run(app, host=app_config.HOST, port=app_config.PORT)
