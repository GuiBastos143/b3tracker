# Dockerfile

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install OS-level dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev gcc

# Create working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Run migrations and start Django dev server (optional, can be overridden in docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]