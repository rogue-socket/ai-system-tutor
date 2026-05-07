# Loop 9 — minimal Cloud Run / serverless image.
# Stage 10 of BREAK.md walks through deploying this.

FROM python:3.11-slim

WORKDIR /app

# uv for fast deps install
RUN pip install --no-cache-dir uv

# Install deps from the locked Group D pyproject. Copy these first for cache.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy the rest of the app
COPY . .

# Cloud Run sets PORT; default 8000 for local docker run
ENV PORT=8000
EXPOSE 8000

# Use the venv's uvicorn
CMD .venv/bin/uvicorn app:app --host 0.0.0.0 --port ${PORT}
