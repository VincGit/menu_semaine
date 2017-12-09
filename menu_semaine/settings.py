"""
Django settings for menu_semaine project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from . import production_credentials
try:
    if os.environ["ENV"] == "local":
        prod = False
        print("Local dev")
    else:
        prod = True
        print("Production phase")
except:
    prod = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8$)i$87l$pz6l!dh8@^f_!$n-vdd9u8dxqj$93#$uqgp#e*%co'

# SECURITY WARNING: don't run with debug turned on in production!
if prod:
    DEBUG = False
else:
    DEBUG = True

if prod:
    ALLOWED_HOSTS = ['vincentlegoff2004.alwaysdata.net']
else:
    ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'menu',
    'sendpdf',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'menu_semaine.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'menu_semaine.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

if prod:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'vincentlegoff2004_menu',
            'USER': production_credentials.production_user,
            'PASSWORD': production_credentials.production_password,
            'HOST': 'mysql-vincentlegoff2004.alwaysdata.net',
            'PORT': '3306',
            'OPTIONS': {
                'sql_mode': 'STRICT_ALL_TABLES'
            }
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-vincentlegoff2004.alwaysdata.net'
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = 'QP_woei0116'
EMAIL_HOST_USER = 'vincentlegoff2004@alwaysdata.net'
DEFAULT_FROM_EMAIL = 'vincentlegoff2004@alwaysdata.net'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

if prod:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
else:
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "static"),
    )


