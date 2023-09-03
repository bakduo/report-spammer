#!/bin/sh

# Make migrations and migrate the database.

export PATH=$PATH:$PATH_APP/.local/bin

python manage.py makemigrations --noinput

python manage.py migrate --noinput

##Control de collec static al menos una vez

if [ -e $PATH_APP/static/app ];then
   CANT=$(ls $PATH_APP/static/app | wc -l)
   if [ $CANT -eq 0 ];then
      python manage.py collectstatic --noinput
   fi
fi

gunicorn authdj.wsgi -b 0.0.0.0:8000 --log-file -

