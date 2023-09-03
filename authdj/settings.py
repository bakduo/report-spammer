"""
Django settings for authdj project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import json

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_APP = {}

with open("config/app.json") as json_data_file:
    CONFIG_APP = json.load(json_data_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = CONFIG_APP['app']['secret'] 


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'


ALLOWED_HOSTS = [CONFIG_APP['app']['website'],'localhost','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', #permite trabajar contenido statico
    'django.contrib.staticfiles',
    'django_mysql',
    'django_bootstrap5',
    'tinymce',
    'rest_framework',
    'corsheaders', #Para controlar la parte del cliente con la API
    'userauth',
    'apis.apps.ApisConfig',
    'spammers',
]

#https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES" : ("rest_framework.permissions.IsAuthenticated",)
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', #parte del paquete cors 
    'whitenoise.middleware.WhiteNoiseMiddleware', # es parte de la app
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

CORS_ALLOWED_ORIGINS = (
    "http://localhost:3000",
    "http://localhost:8000",
    "https://"+str(CONFIG_APP['app']['website']),
    "http://"+str(CONFIG_APP['app']['website']),
)

CORS_ORIGIN_WHITELIST = (
    "http://localhost:3000",
    "http://localhost:8000",
)

#Caso de tener un front extra
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://"+str(CONFIG_APP['app']['website']),
    "https://"+str(CONFIG_APP['app']['website']),
]

ROOT_URLCONF = 'authdj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR.joinpath('templates'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'authdj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': CONFIG_APP['app']["db1"]['ENGINE'],
        "NAME": CONFIG_APP['app']["db1"]['dbname'],
        "USER": CONFIG_APP['app']["db1"]['user'],
        "PASSWORD": CONFIG_APP['app']["db1"]['passwd'],
        "HOST": CONFIG_APP['app']["db1"]['host'],
        "PORT": CONFIG_APP['app']["db1"]['port'],
    },
    'OPTIONS': {
            'init_command': CONFIG_APP['app']["db1"]['init_command'],
            "charset": CONFIG_APP['app']["db1"]['charset'],
        },
        "TEST": {
            "CHARSET": "utf8mb4",
            "COLLATION": "utf8mb4_unicode_ci",
        },
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


#https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-FILE_UPLOAD_HANDLERS
#https://docs.djangoproject.com/en/4.2/topics/http/file-uploads/
FILE_UPLOAD_HANDLERS = [
    
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = CONFIG_APP['app']["language"]

TIME_ZONE = CONFIG_APP['app']["timezone"]

USE_I18N = True

USE_TZ = True

## Agrega soporte para log

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s',
             'datefmt': '%y %b %d, %H:%M:%S',
            },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'celery': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True
        },
    },
}


## Fin soporte de log



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

APP_FIX= 'app/'

# Agrega soporte para static dirs

STATICFILES_DIRS = (str(BASE_DIR.joinpath('static')),)

# Para production es STATIC_ROOT

STATIC_ROOT = str(BASE_DIR.joinpath('static/app'))

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage" # Permite realizar compile static

# fin para production

# Agrega soporte para decirle a django como buscar staticfiles

STATICFILES_FINDER = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder"
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

##Agrega soporte para auth user custom
AUTH_USER_MODEL="userauth.CustomUser"

##Agrega redirect default
LOGIN_REDIRECT_URL="home"
##Agrega redirect logout
LOGOUT_REDIRECT_URL="home"

SILENCED_SYSTEM_CHECKS = [
  "django_mysql.W003",
]

TINYMCE_JS_URL = os.path.join(STATIC_URL, APP_FIX+"tinymce/tinymce.min.js")
TINYMCE_JS_ROOT = os.path.join(STATIC_URL, APP_FIX+"tinymce/")

TINYMCE_DEFAULT_CONFIG = {
  'cleanup_on_startup': True,
  "selector": 'textarea',
  "height": 250,
  "menu": {
    "edit": {"title": 'Edit', "items": 'undo, redo, selectall'}
  },
  "toolbar": 'undo redo | formatselect | ' +
  'bold italic backcolor | alignleft aligncenter ' +
  'alignright alignjustify | bullist numlist outdent indent | ' +
  'removeformat | help',
  "content_style": 'body { font-family:Helvetica,Arial,sans-serif; font-size:14px }',
  'spellchecker_languages': 'en,es,fi,fr,da,de,nl,it,nb,pt,sv,zh',
}
