Spam report
===========

Permite realizar reporte de mails como spam.

## summary

- [x] soporte para MySQL
- [x] soporte para PostgreSQL con minima re-configuration
- [x] soporte para build image docker
- [x] Agrega soporte para API Rest para listar y para acceso individuales por id solo con autenticación.
- [x] Add sitemap.
- [x] soporte para whitenoise.
- [x] Soporte con https
- [x] sitio => https://report-spam.oncosmos.com
  
```

Ejemplo de configuración config/app.json

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
        "debug":"False",
        "uploadfolder":"/path-static"
    }
}

Estructura statica:

static/
├── app
│   ├── admin
│   ├── css
│   ├── django_tinymce
│   ├── images
│   ├── js
│   ├── rest_framework
│   ├── staticfiles.json
│   └── tinymce
├── css
│   └── base.css
├── images
│   └── logo.png
└── js
    └── base.js


Generate user:

python manage.py createsuperuser --username user --email user@domain.tld

Permitir ejecutar dev:

mkdir log && mkdir config && mkdir eml && mkdir -p */migrations/

Luego generar:

touch */migrations/__init__.py

Put your config app and:

./rundev.sh

Permite ejecutar prod via proxy pass:

./run-gunicorn.sh

Build app:

make build

Testing:

python manage.py test

```