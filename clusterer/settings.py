# -*- coding: utf-8 -*-
# clusterer settings
# copyright 2014 Chibwe Ltd

"""
Django settings for reuben project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from unipath import Path
import djcelery

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!jp+8b_^+5)18^k7hll&vgiz2-b5_l-=99=t%p0bkhed(s&e-u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'getdata',
    'bootstrap3',
    'registration',
    'usedata',
    'djcelery',
    'django_ses',
    'django.contrib.humanize',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


#####
#  S3 Storage
#####

DEFAULT_FILE_STORAGE = 'clusterer.s3utils.MediaS3BotoStorage'
STATICFILES_STORAGE = 'clusterer.s3utils.StaticS3BotoStorage'
AWS_ACCESS_KEY_ID = 'AKIAJSHND5LSYK4XR47Q'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'osmium'
S3_URL = 'http://%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
STATIC_DIRECTORY = '/static/'
MEDIA_DIRECTORY = '/media/'
STATIC_URL = S3_URL + STATIC_DIRECTORY
MEDIA_URL = S3_URL + MEDIA_DIRECTORY

POSTMARK_API_KEY = '837cc6b1-5112-4faa-a2ef-b5fc7b7bc187'
POSTMARK_SENDER = 'nigel@chibwe.com'


DEFAULT_FROM_EMAIL = 'nigel@chibwe.com'


ROOT_URLCONF = 'clusterer.urls'

WSGI_APPLICATION = 'clusterer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':  'cluster_db',
        'USER': 'django_login',
        'PASSWORD': 'BigRock56789',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


BROKER_URL = 'redis://localhost:6379/0'
CELERY_IMPORTS = ('usedata.tasks',)
djcelery.setup_loader()

# Static asset configuration
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
PROJECT_DIR = Path(PROJECT_ROOT).parent

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

TEMP_ROOT = os.path.join(PROJECT_ROOT, 'temp')
TEMP_URL = '/temp/'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    PROJECT_DIR.child("templates"),
)
