# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app


# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . .

COPY scenic-setup-455312-h1-d5a2ac6a7496.json /app/gcp-key.json

# Set entrypoint
CMD ["gunicorn", "moderation_service.wsgi:application", "--bind", "0.0.0.0:8000"]
