"""
Django settings for com_jrdbnntt_wedding project.

Generated by 'django-admin startproject' using Django 3.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import datetime
import ntpath
import os
import pathlib
from pathlib import Path

from com_jrdbnntt_wedding import config
from com_jrdbnntt_wedding import logs

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

active_config = config.load()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = active_config.get(config.SECTION_DJANGO, 'SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = active_config.getboolean(config.SECTION_DJANGO, 'DEBUG')
LOGGING = logs.build_django_config(DEBUG)

ALLOWED_HOSTS = active_config.get(config.SECTION_DJANGO, 'ALLOWED_HOSTS').split(',')

# Front-end file management with webpack
STATICFILES_DIRS = (
    BASE_DIR / 'website/static/build',
    BASE_DIR / 'website/static/cloud'
)
WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': '',  # must end with slash
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map'],
        'LOADER_CLASS': 'webpack_loader.loader.WebpackLoader',
    }
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',
    'webpack_loader',
    'website.apps.WebsiteConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'com_jrdbnntt_wedding.urls'

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'website/src/views'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'website.context_processors.add_global_vars',
                'website.context_processors.set_navigation_options'
            ],
        },
    },
]

WSGI_APPLICATION = 'com_jrdbnntt_wedding.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': active_config.get(config.SECTION_DATABASE, 'HOST'),
        'PORT': active_config.getint(config.SECTION_DATABASE, 'PORT'),
        'NAME': active_config.get(config.SECTION_DATABASE, 'NAME'),
        'USER': active_config.get(config.SECTION_DATABASE, 'USER'),
        'PASSWORD': active_config.get(config.SECTION_DATABASE, 'PASSWORD')
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
STATIC_ROOT = active_config.get(config.SECTION_DJANGO, 'STATIC_ROOT')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security
SECURE_SSL_REDIRECT = active_config.getboolean(config.SECTION_DJANGO, 'SECURE_SSL_REDIRECT')
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = active_config.getint(config.SECTION_DJANGO, 'SECURE_HSTS_SECONDS')
SECURE_HSTS_PRELOAD = active_config.getboolean(config.SECTION_DJANGO, 'SECURE_HSTS_PRELOAD')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
ADMIN_SITE_ENABLED = active_config.getboolean(config.SECTION_DJANGO, 'ADMIN_SITE_ENABLED')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# reCAPTCHA
RECAPTCHA_SITE_KEY = active_config.get(config.SECTION_RECAPTCHA, 'SITE_KEY')
config.assert_defined(config.SECTION_RECAPTCHA, 'SITE_KEY', RECAPTCHA_SITE_KEY)
RECAPTCHA_SECRET_KEY = active_config.get(config.SECTION_RECAPTCHA, 'SECRET_KEY')
config.assert_defined(config.SECTION_RECAPTCHA, 'SECRET_KEY', RECAPTCHA_SECRET_KEY)
RECAPTCHA_ENABLED = active_config.getboolean(config.SECTION_RECAPTCHA, 'ENABLED')

# Email configuration (SendGrid)
EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
SENDGRID_SANDBOX_MODE_IN_DEBUG = active_config.getboolean(config.SECTION_EMAIL, 'SENDGRID_SANDBOX_MODE_IN_DEBUG')
SENDGRID_API_KEY = active_config.get(config.SECTION_EMAIL, 'SENDGRID_API_KEY')
config.assert_defined(config.SECTION_EMAIL, 'SENDGRID_API_KEY', SENDGRID_API_KEY)
EMAIL_HOST = active_config.get(config.SECTION_EMAIL, 'EMAIL_HOST')
EMAIL_HOST_USER = active_config.get(config.SECTION_EMAIL, 'EMAIL_HOST_USER')
if EMAIL_HOST_USER is None or EMAIL_HOST_USER == "":
    EMAIL_HOST_USER = SENDGRID_API_KEY
EMAIL_HOST_PASSWORD = active_config.get(config.SECTION_EMAIL, 'EMAIL_HOST_PASSWORD')
EMAIL_PORT = active_config.get(config.SECTION_EMAIL, 'EMAIL_PORT')

# Email message settings
EMAIL_FROM_DEFAULT = active_config.get(config.SECTION_EMAIL, 'EMAIL_FROM_DEFAULT')
config.assert_defined(config.SECTION_EMAIL, 'EMAIL_FROM_DEFAULT', EMAIL_FROM_DEFAULT)
EMAIL_LINK_BASE_URL = active_config.get(config.SECTION_EMAIL, 'EMAIL_LINK_BASE_URL')
config.assert_defined(config.SECTION_EMAIL, 'EMAIL_LINK_BASE_URL', EMAIL_LINK_BASE_URL)

# Event details
EVENT_DATE = datetime.datetime.fromisoformat(active_config.get(config.SECTION_EVENT_DETAILS, 'DATE'))
DATE_RSVP_DEADLINE = datetime.datetime.fromisoformat(
    active_config.get(config.SECTION_EVENT_DETAILS, 'DATE_RSVP_DEADLINE'))
EVENT_PUBLIC_LOCATION = active_config.get(config.SECTION_EVENT_DETAILS, 'PUBLIC_LOCATION')

# Tasks
MIN_TIME_BETWEEN_TASK_POLLING_IN_SECONDS = active_config.getfloat(config.SECTION_TASKS,
                                                                  'MIN_TIME_BETWEEN_TASK_POLLING_IN_SECONDS')
REAP_OLD_TASKS_AFTER_SECONDS = active_config.getfloat(config.SECTION_TASKS, 'REAP_OLD_TASKS_AFTER_SECONDS')
CANCEL_TASKS_AFTER_SECONDS = active_config.getint(config.SECTION_TASKS, 'CANCEL_TASKS_AFTER_SECONDS')
