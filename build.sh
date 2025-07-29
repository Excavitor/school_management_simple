#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Specify your production settings
export DJANGO_SETTINGS_MODULE=school_management.settings.prod

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate