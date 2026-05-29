# Use Python 3.12 to perfectly match your local lockfile
FROM python:3.12-slim-bookworm

# Grab 'uv' directly from their official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy your dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies and create the .venv in one single step
RUN uv sync --frozen --no-install-project --no-dev

# Add the new virtual environment to the system path
ENV PATH="/app/.venv/bin:$PATH"

# Copy your code and the model
COPY wine_quality_api.py .
COPY models/wine_quality_model.pkl ./models/

# Run it explicitly using the python interpreter
CMD ["python", "-m", "uvicorn", "wine_quality_api:app", "--host", "0.0.0.0", "--port", "8000"]