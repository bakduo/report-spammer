Spam report
===========0

This app permit report an email spammer and attach eml for MUA agent.

## summary

- [x] support MySQL
- [x] support PostgreSQL with minimal re-configuration
- [x] support Docker build
- [x] support API Rest only for list and list individual message with auth.
  
```

Example configuration config/app.json

{
    "app":{
        "secret":"django-insecure-secret",
        "website":"site.domain.tld",
        "timezone":"your timezone ",
        "language":" yout language",
        "db1":{
            "ENGINE":"django.db.backends.mysql",
            "dbname":"sample",
            "user":"sample",
            "passwd":"sample",
            "host":"localhost",
            "port":3306,
            "init_command":"'SET innodb_strict_mode=1'",
            "charset":"utf8mb4"
        }
    }
}


Generate user:

python manage.py createsuperuser --username user --email user@domain.tld

Permitir ejecutar dev:

mkdir log && mkdir config && mkdir eml

Put your config app and:

./rundev.sh

Permite ejecutar semi-prod:

./run-gunicorn.sh

Build app:

make build

Testing:

python manage.py test

```