#!/usr/bin/env bash
# exit on error
set -o errexit

# Add this line to specify your production settings
export DJANGO_SETTINGS_MODULE=school_management.settings.prod

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate