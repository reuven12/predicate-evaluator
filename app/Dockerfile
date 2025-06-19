# Stage 1: Base layer for both app and tests
FROM python:3.11-slim AS base

WORKDIR /app
ENV PYTHONUNBUFFERED=1

# Install runtime dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Stage 2: App runtime image
FROM base AS app

CMD ["python","-u", "main.py"] 

# Stage 3: Test image
FROM base AS test

# Install test-only dependencies
COPY requirements-test.txt .
RUN pip install --no-cache-dir -r requirements-test.txt

CMD ["pytest", "--tb=short", "--maxfail=3"]
