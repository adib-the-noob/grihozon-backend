FROM python:3.14-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml .
RUN pip install --upgrade pip && pip install .

# Install curl for health checks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy project
COPY . .

# Copy and set permissions for entrypoint scripts
COPY entrypoint.sh /entrypoint.sh
COPY celery-entrypoint.sh /celery-entrypoint.sh
RUN chmod +x /entrypoint.sh /celery-entrypoint.sh

# Set work directory to app folder
WORKDIR /app/app

# Expose port
EXPOSE 8000

# Default entrypoint (web service)
ENTRYPOINT ["/entrypoint.sh"]

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
