# =============================================================================
# Dockerfile for Real Estate CRM Django Application
# Optimized for Azure Web App for Containers
# =============================================================================

# Stage 1: Base image with Python
FROM python:3.11-slim as base

# Prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# =============================================================================
# Stage 2: Dependencies
# =============================================================================
FROM base as dependencies

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# =============================================================================
# Stage 3: Development image
# =============================================================================
FROM dependencies as development

# Set environment variables for development
ENV DJANGO_DEBUG=True
ENV DJANGO_SETTINGS_MODULE=realestate_crm.settings

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Run development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# =============================================================================
# Stage 4: Production image (for Azure)
# =============================================================================
FROM dependencies as production

# Set environment variables for production
ENV DJANGO_DEBUG=False
ENV DJANGO_SETTINGS_MODULE=realestate_crm.settings
ENV PORT=8000

# Create non-root user for security
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --gid 1001 --no-create-home appuser

# Copy project files
COPY --chown=appuser:appgroup . .

# Create directories for static files and data
RUN mkdir -p /app/staticfiles /app/data && \
    chown -R appuser:appgroup /app/staticfiles /app/data

# Collect static files
RUN python manage.py collectstatic --no-input

# Switch to non-root user
USER appuser

# Expose port (Azure uses PORT env variable)
EXPOSE 8000

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Run migrations and start gunicorn
# Azure Web App expects the container to listen on PORT
CMD python manage.py migrate --no-input && \
    gunicorn --bind 0.0.0.0:${PORT:-8000} --workers 2 --threads 4 --timeout 120 realestate_crm.wsgi:application