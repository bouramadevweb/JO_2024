"""
Django settings for JeuxOlympique project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

import os
from pickle import FALSE
import django_heroku
import dj_database_url
from  decouple import config

import my_app_jo


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = os.path.join(BASE_DIR, 'data')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-z$6(o!_gyn&og3tusy-lit^4s)#21hqh20eq&c05ft@93g8pj4'
SECRET_KEY = config('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = os.environ.get("DEBUG","False")== "True"

# ALLOWED_HOSTS = ['jeuxolympique-ababa0c1b617.herokuapp.com']
IS_HEROKU_APP = "DYNO" in os.environ and not "CI" in os.environ


if IS_HEROKU_APP:
    ALLOWED_HOSTS = ["https://jeuxolympique-ababa0c1b617.herokuapp.com/"]
else:
    ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'my_app_jo',
    'administration',
    'bootstrap4',
    'django_twilio',
    'whitenoise.runserver_nostatic'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    
]

ROOT_URLCONF = 'JeuxOlympique.urls'



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        # 'DIRS': [TEMPLATES_DIR],

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

WSGI_APPLICATION = 'JeuxOlympique.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "Olympique",
#         "USER": "postgres",
#         "PASSWORD": "kungfu",
#         "HOST": "localhost",
#         "PORT": "5432",
#     }
# }
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "d3hakkjh8d40tg",
#         "USER": "u71jj16hv9q4vu",
#         "PASSWORD": "p4944a9cc23366839f71da4bfe78969d759af518a7d521b78c388f26caceaf052",
#         "HOST": "cdgn4ufq38ipd0.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com",
#         "PORT": "5432",
#         "URI":   "postgres://u71jj16hv9q4vu:p4944a9cc23366839f71da4bfe78969d759af518a7d521b78c388f26caceaf052@cdgn4ufq38ipd0.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/d3hakkjh8d40tg"


#     }
# }
DATABASES = {
    "default": dj_database_url.parse(config('DATABASE_URL'))
}

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_S3_SIGNATURE_NAME = 'S3V4'
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_REGION_NAME = config('AWS_REGION')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
# settings.py

AUTH_USER_MODEL = 'my_app_jo.User'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATIC_URL = 'static/'
# MEDIA_URL = '/media/'
# STATICFILES_DIR = [BASE_DIR,'static']
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]
# MEDIA_URL ='/'
# MEDIA_ROOT = os.path.join(BASE_DIR,'media')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configuration des fichiers statiques
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
django_heroku.settings(locals()),
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
# Configuration des fichiers média
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary k ey field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL ='/'

# ENVIRONMENT == 'production' or POSTGRESLOCALLY == TRUE 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
ACCOUNT_AUTHENTICATION_METHOD ='email'
ACCOUNT_EMAIL_REQUIRED =True
EMAIL_HOST = 'smtp.gmail.com'   # env('EMAIL_ADDRESS')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'bouramadevweb@gmail.com'  
EMAIL_HOST_PASSWORD = '240283KungfuMaitre' 
ACCOUNT_AUTHENTICATION_BLACKLIST = ['admin','accounts','connexion']

import os
from dotenv import load_dotenv

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv()

# Utilisation des variables d'environnement
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
