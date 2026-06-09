#!/usr/bin/env bash
set -o errexit

# Retry migration up to 3 times (handles DB not ready on first boot)
MIGRATED=false
for i in 1 2 3; do
    if python manage.py migrate --noinput; then
        MIGRATED=true
        break
    fi
    sleep 3
done

if [ "$MIGRATED" = false ]; then
    echo "Migrations failed after 3 retries — exiting"
    exit 1
fi

python scripts/seed_data.py

gunicorn hms.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --timeout 120 --access-logfile - --error-logfile -
