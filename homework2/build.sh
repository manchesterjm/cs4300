#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# collect static assets
python manage.py collectstatic --noinput

# run database migrations
python manage.py migrate --noinput
