FROM python:3.10-slim-bullseye

WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --only main

COPY . .

RUN poetry install --only main

CMD ["poetry", "run", "forwarder"]
