#!/bin/bash
python manage.py collectstatic --pythonpath src --noinput
python manage.py migrate --pythonpath src --noinput
python manage.py createsuperuser --pythonpath src --noinput --name admin --email admin@example.com
