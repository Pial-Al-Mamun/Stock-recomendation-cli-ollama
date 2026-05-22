FROM ghcr.io/astral-sh/uv:python3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies (no pip; uses built-in uv)
COPY pyproject.toml /app/
RUN uv sync --no-dev

# Copy the application code
COPY . /app

CMD ["uv", "run", "python", "main.py"]
