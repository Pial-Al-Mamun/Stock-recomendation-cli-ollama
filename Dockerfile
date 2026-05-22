FROM ghcr.io/astral-sh/uv:python3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies (no pip; uses uv + uv.lock)
COPY pyproject.toml uv.lock /app/
RUN uv sync --frozen --no-dev

# Copy the application code
COPY . /app

CMD ["uv", "run", "python", "main.py"]
