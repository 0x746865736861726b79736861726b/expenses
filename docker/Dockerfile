FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    mv /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry install --no-dev --no-root

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "python", "apps/manage.py", "runserver", "0.0.0.0:8000"]
