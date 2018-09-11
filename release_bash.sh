#!/bin/bash
cd src/
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate --noinput
# Run this only in your first deployment
#python manage.py createsuperuser --noinput --name dsdsaadmin1 --email dsdsaadmin1@example.com
