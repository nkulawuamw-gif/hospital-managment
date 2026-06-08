#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

mkdir -p logs media staticfiles

python manage.py collectstatic --noinput --clear
python manage.py migrate --noinput
