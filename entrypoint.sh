#!/bin/sh

# Make migrations and migrate the database.
export PATH=$PATH:/home/app/.local/bin
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn authdj.wsgi --log-file -
