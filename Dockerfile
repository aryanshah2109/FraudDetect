# Python dependency
FROM python:3.12-slim

# Python optimization
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /app

# Install system dependency
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install system dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy and install developer dependencies
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copy entire project
COPY . .

# Expose FastAPI port
EXPOSE 8000

# RUN API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]