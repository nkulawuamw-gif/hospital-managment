#!/usr/bin/env bash
set -o errexit

python manage.py migrate --noinput
gunicorn hms.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --timeout 120 --access-logfile - --error-logfile -
