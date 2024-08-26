FROM python:3.12-slim as builder

# set env variables
ENV APP_HOME=/app \
    PDM_HOME=/opt/pdm \
    PYTHONUNBUFFERED=1 \
    C_FORCE_ROOT=1

WORKDIR $APP_HOME

# install pdm
RUN python -m venv $PDM_HOME
RUN $PDM_HOME/bin/pip install pdm

# copy project files
COPY . $APP_HOME/

# install dependencies
RUN $PDM_HOME/bin/pdm install -g -p ${APP_HOME}

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]