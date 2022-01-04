"""
Django settings for com_jrdbnntt_wedding project.

Generated by 'django-admin startproject' using Django 3.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from configparser import ConfigParser
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Read in environment configuration settings
os.environ.setdefault('RUNTIME_ENVIRONMENT', 'DEVELOPMENT')
RUNTIME_ENVIRONMENT = os.environ.get('RUNTIME_ENVIRONMENT')
print("Configuring for runtime: ", RUNTIME_ENVIRONMENT)

# Read config for environment
CONFIG_SECTION_DJANGO = 'django'
config = ConfigParser()
CONFIG_FILE_DIR = Path(BASE_DIR, 'com_jrdbnntt_wedding/config')
CONFIG_FILES = {
    'base': Path(CONFIG_FILE_DIR, 'base.cfg'),
    'PRODUCTION': Path(CONFIG_FILE_DIR, 'production.cfg'),
    'TEST': Path(CONFIG_FILE_DIR, 'test.cfg'),
    'DEVELOPMENT': Path(CONFIG_FILE_DIR, 'development.cfg')
}
config_file = CONFIG_FILES[RUNTIME_ENVIRONMENT]
print("Loading base config file: ", CONFIG_FILES['base'])
if not config_file.exists():
    raise EnvironmentError("Missing config file: ", config_file.absolute())
config.read(CONFIG_FILES['base'])
if RUNTIME_ENVIRONMENT in CONFIG_FILES.keys():
    config_file = CONFIG_FILES[RUNTIME_ENVIRONMENT]
    print("Loading {} environment config file: {}".format(RUNTIME_ENVIRONMENT, config_file.absolute()))
    if not config_file.exists():
        raise EnvironmentError("Missing config file: ", config_file.absolute())
    config.read(config_file)
else:
    raise EnvironmentError('Invalid RUNTIME_ENVIRONMENT')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get(CONFIG_SECTION_DJANGO, 'SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.getboolean(CONFIG_SECTION_DJANGO, 'DEBUG')

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'com_jrdbnntt_wedding.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'website/templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'website.context_processors.add_global_vars'
            ],
        },
    },
]

WSGI_APPLICATION = 'com_jrdbnntt_wedding.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
