# ==========================================
# Stage 1: Build & Dependencies
# ==========================================
FROM python:3.11-alpine AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install build dependencies for compiling any C extensions
RUN apk add --no-cache build-base libffi-dev

# Create dedicated virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip and build tools
RUN pip install --no-cache-dir --upgrade pip "setuptools>=83.0.0" "wheel>=0.46.2"

COPY pyproject.toml requirements.txt ./

# Install application dependencies and enforce safe msgpack
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir --upgrade "msgpack>=1.2.1"

# Strip all build-only package metadata from /opt/venv
RUN rm -rf /opt/venv/lib/python3.11/site-packages/setuptools* \
    /opt/venv/lib/python3.11/site-packages/wheel* \
    /opt/venv/lib/python3.11/site-packages/pip*

# ==========================================
# Stage 2: Minimal Production Runtime (Alpine)
# ==========================================
FROM python:3.11-alpine AS runner

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Install curl for health checks and apply latest security patches
RUN apk update && \
    apk upgrade --no-cache && \
    apk add --no-cache curl && \
    rm -rf /var/cache/apk/* && \
    rm -rf /usr/local/lib/python3.11/site-packages/* \
    /usr/local/lib/python3.11/ensurepip

# Create non-root system user and group
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

# Copy sanitized virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application source code directly with correct ownership
COPY --chown=appuser:appgroup . .

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
