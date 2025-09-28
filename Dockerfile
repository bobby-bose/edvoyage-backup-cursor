# Base image
FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y poppler-utils build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Set work directory inside container
WORKDIR /app

# Copy only requirements first for caching
COPY backend/edvoayge/requirements.txt ./requirements.txt

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of your Django project
COPY backend/edvoayge/ ./edvoayge

# Set environment variable for Django
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=edvoayge.settings
ENV POPPLER_PATH=/usr/bin

# Collect static files
RUN python ./edvoayge/manage.py collectstatic --noinput

# Expose port for Render
EXPOSE 8000

# Start Gunicorn
CMD ["gunicorn", "edvoayge.wsgi:application", "--bind", "0.0.0.0:$PORT"]
