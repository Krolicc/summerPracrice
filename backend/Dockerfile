FROM python:3.13

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry cache clear --all pypi && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --only main

COPY . .

EXPOSE 8000

ENTRYPOINT ["sh", "-c", "poetry run alembic upgrade head && poetry run uvicorn main:application --host 0.0.0.0 --port 8000 --reload"]
