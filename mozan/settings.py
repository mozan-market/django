"""
Django settings for mozan project.
For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nmm9!*%lsr)yrjitsv540q%b&pdnn7vf1lsgox8ic9@ydmy54e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',            #databse sync and migrate
    'mozan_app',
    'mptt',             #Categories
    'rest_framework',   #DRF
    'rest_framework.authtoken',  # Token authorization
    'haystack',         #search
    'hitcount',         #count post views
    'sms_signup',
)

from rest_framework.settings import api_settings

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}


HAYSTACK_CONNECTIONS = {
    'default': {
    'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
    'URL': 'http://127.0.0.1:9200/',
    'INDEX_NAME': 'haystack',
    },
}

# The three variables to configure the module.
HITCOUNT_KEEP_HIT_ACTIVE = { 'days': 1 }
HITCOUNT_HITS_PER_IP_LIMIT = 0
HITCOUNT_EXCLUDE_USER_GROUP = ( 'Staff', )

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mozan.urls'

WSGI_APPLICATION = 'mozan.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
# see local settings



# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Asia/Bishkek'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

#LOGIN_URL = '/'
TEMPLATE_DIRS = ( os.path.join(BASE_DIR, 'templates'), )

# Import settings
from settings_local import *

