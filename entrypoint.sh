#!/bin/sh

# Make migrations and migrate the database.
export PATH=$PATH:/home/app/.local/bin
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic -c --noinput
gunicorn authdj.wsgi -b 0.0.0.0:8000 --log-file -

