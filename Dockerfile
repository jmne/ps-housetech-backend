FROM python:3.11.3-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.4.2  \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/app" \
    VENV_PATH="/app/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

###############################################
# Builder Image
###############################################
FROM python-base as builder-base
RUN apt-get update && apt-get install --no-install-recommends -y curl gunicorn

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=$POETRY_VERSION python -
RUN export PATH=/opt/poetry/bin:$PATH

# copy project requirement files here to ensure they will be cached.
COPY ./ ./app
WORKDIR ./app

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry config installer.max-workers 10

RUN poetry install --no-interaction

CMD [".venv/bin/gunicorn", "src.run:app", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120", "-n", "ps-housetech-backend"]
