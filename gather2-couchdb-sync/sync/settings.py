"""
Django settings for gather2_couchdb_sync project.

Generated by 'django-admin startproject' using Django 1.8.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import logging
logger = logging.getLogger(__name__)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def here(x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), x)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$%7as98^%*OgJYabsiyAyqfif65*_d43!c)3-7-$9f3ii%2z#^dox!rjhg6uw_a2$_3(wv'

# SECURITY WARNING: this should also be considered a secret:
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', '')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]
CSRF_COOKIE_DOMAIN = '.ehealthafrica.org'
CSRF_TRUSTED_ORIGINS = [".ehealthafrica.org"]

# # Tell django to view requests as secure(ssl) that have this header set
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# USE_X_FORWARDED_HOST = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'django_cas_ng',
    'ums_client',
    'api',
    'importer',
    'django_rq',
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
    'corsheaders.middleware.CorsMiddleware',
)

FIXTURE_DIRS = (
    'fixtures/',
)

ROOT_URLCONF = 'sync.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'sync.wsgi.application'

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
STATIC_ROOT = os.environ.get("STATIC_ROOT", here('../static_root'))


MEDIA_ROOT = here('../media_root')
MEDIA_URL = '/media/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('RDS_DB_NAME', 'couchdb_sync'),
        'PASSWORD': os.environ.get('RDS_PASSWORD', ''),
        'USER': os.environ.get('RDS_USERNAME', 'postgres'),
        'HOST': os.environ.get('RDS_HOSTNAME', 'db'),
        'PORT': os.environ.get('RDS_PORT', '5432'),
    }
}

COUCHDB_URL = os.environ.get('COUCHDB_URL', 'http://couchdb:5984')
COUCHDB_USER = os.environ.get('COUCHDB_USER', None)
COUCHDB_PASSWORD = os.environ.get('COUCHDB_PASSWORD', None)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    )
}

# Allow cors for all origins but only for the sync endpoint
CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/sync/.*$'

GATHER_CORE_URL = os.environ.get('GATHER_CORE_URL')
GATHER_CORE_TOKEN = os.environ.get('GATHER_CORE_TOKEN')


def test_gather_core_connection():
    import requests
    return requests.get(GATHER_CORE_URL + '/surveys.json',
                        headers={'Authorization': 'Token {}'.format(GATHER_CORE_TOKEN)})


if GATHER_CORE_URL and GATHER_CORE_TOKEN:
    try:
        r = test_gather_core_connection()
        assert r.status_code == 200, r.content
        logger.info('GATHER_CORE_URL and GATHER_CORE_TOKEN are valid', )
    except Exception as e:
        logger.exception(
            "GATHER_CORE_URL and GATHER_CORE_TOKEN are not valid, saving XForm responses will not work: {}".format(GATHER_CORE_URL))
else:
    logger.warning(
        'GATHER_CORE_URL and GATHER_CORE_TOKEN are not set, saving XForm responses will not work.')

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # this is default
    'ums_client.backends.UMSRoleBackend'
)

CAS_SERVER_URL = os.environ.get(
    "CAS_SERVER_URL", "https://ums-dev.ehealthafrica.org")
HOSTNAME = os.environ.get("HOSTNAME", "localhost")
CAS_VERSION = 3
CAS_LOGOUT_COMPLETELY = True

CORS_ORIGIN_ALLOW_ALL = True

if os.environ.get('DJANGO_USE_X_FORWARDED_HOST', False):
    USE_X_FORWARDED_HOST = True

if os.environ.get('DJANGO_USE_X_FORWARDED_PORT', False):
    USE_X_FORWARDED_PORT = True

if os.environ.get('DJANGO_HTTP_X_FORWARDED_PROTO', False):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Import processing
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
REDIS_DB = os.environ.get('REDIS_DB', 0)
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)


# RQ

RQ_QUEUES = {
    'default': {
        'HOST': REDIS_HOST,
        'PORT': REDIS_PORT,
        'DB': REDIS_DB,
        'PASSWORD': REDIS_PASSWORD,
        'DEFAULT_TIMEOUT': 360,
    },
}
RQ_SHOW_ADMIN_LINK = True