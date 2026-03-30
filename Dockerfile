# ============================================================
# Battery SOH Prediction - Complete Docker Image
# ============================================================
# This Dockerfile creates a standalone container with:
# - FastAPI backend server
# - Web frontend interface
# - Pre-trained ML model
# - SOH-band disposal / lab-safety guidance (GET /disposal/ranges, included in POST /predict)
# - All dependencies included
#
# Works on: Windows, macOS, Linux (any OS with Docker)
# ============================================================

# ============== Build Stage ==============
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements-api.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-api.txt

# ============== Runtime Stage ==============
FROM python:3.11-slim AS runtime

WORKDIR /app

# Create non-root user for runtime security
RUN useradd --create-home --shell /bin/bash appuser

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY api/ ./api/
COPY src/ ./src/
COPY models/ ./models/
COPY frontend/ ./frontend/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app
ENV PORT=8000
ENV WEB_CONCURRENCY=2
ENV LOG_LEVEL=info

# Ensure runtime user can access app files
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check using Python stdlib (no curl dependency)
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=5)"

# Labels for documentation
LABEL maintainer="Kumar"
LABEL version="1.0.0"
LABEL description="Battery SOH Prediction API with Web Frontend and SOH-based disposal guidance"
LABEL org.opencontainers.image.description="Li-ion SOH API: predictions, recommendations, disposal/analysis precautions by SOH band"

# Run server with production worker manager
CMD ["gunicorn", "api.main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120", "--graceful-timeout", "30", "--keep-alive", "5", "--access-logfile", "-", "--error-logfile", "-"]
