#!/bin/bash
cd src/
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py createsuperuser --noinput --name admin --email admin@example.com
