#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e



echo "Updating system packages..."
apt-get update

echo "Installing system dependencies: Poppler, build tools, PostgreSQL dev..."
apt-get install -y poppler-utils build-essential libpq-dev

echo "Upgrading pip..."
pip install --upgrade pip
# Change directory to your Django project
cd backend/edvoayge

echo "Installing Python dependencies from requirements.txt..."

pip install -r requirements.txt

echo "Collecting Django static files..."
python manage.py collectstatic --noinput

echo "Starting Django development server on 0.0.0.0:8000..."
python manage.py runserver 0.0.0.0:8000
