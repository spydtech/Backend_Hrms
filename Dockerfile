# Python base image
FROM python:3.12-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml ./
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini ./

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install .

# Create uploads directory
RUN mkdir -p /app/uploads

# Application port
EXPOSE 8000

# Run FastAPI as root (default Docker user)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]