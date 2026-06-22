#!/bin/bash 
python manage.py collectstatic --noinput 
python manage.py migrate --noinput 
gunicorn your nitin_deploy.wsgi:application --bind 0.0.0.0:$PORT 