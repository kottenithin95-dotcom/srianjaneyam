#!/bin/bash
python manage.py collectstatic --noinput
python manage.py migrate --noinput
gunicorn nitin_deploy.wsgi:application --bind 0.0.0.0:$PORT