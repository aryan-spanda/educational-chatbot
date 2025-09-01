# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser -u 1001 appuser

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY *.py ./
COPY faiss_index/ ./faiss_index/

# Create necessary directories and set permissions
RUN mkdir -p /app/data/faiss_index /app/data/documents /tmp && \
    chown -R appuser:appuser /app /tmp

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run uvicorn server when the container launches
CMD ["uvicorn", "main_api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
