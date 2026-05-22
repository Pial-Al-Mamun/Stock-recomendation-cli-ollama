FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install uv (fast dependency installer) inside the image
RUN pip install --no-cache-dir uv

# Install Python deps from pyproject.toml
COPY pyproject.toml /app/pyproject.toml
RUN python -c "import tomllib, pathlib; deps=tomllib.loads(pathlib.Path('pyproject.toml').read_text())['project'].get('dependencies', []); print('\\n'.join(deps))" > /tmp/requirements.txt \
    && uv pip install --system --no-cache -r /tmp/requirements.txt \
    && rm -f /tmp/requirements.txt

# Copy the application code
COPY . /app

CMD ["python", "main.py"]
