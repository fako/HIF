import os
import logging

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from datascope.configuration import environment
from datascope.version import get_project_version


log = logging.getLogger(__name__)


#######################################################
# DEFAULT BOOTSTRAP
#######################################################

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The version of the entire project (frontend and backend)
DATASCOPE_VERSION = get_project_version(os.path.join(BASE_DIR, "package.json"))

URL_TO_PROJECT = '/'  # Wikipedia specific probably
USE_WEBSOCKETS = False
STATIC_IP = ""
USE_MOCKS = False

# Wikipedia specific hack to fix prefixes of paths
# Probably couldn't use SCRIPT_NAME properly in that environment
# But can't remember exactly ...
SEGMENTS_BEFORE_PROJECT_ROOT = len([segment for segment in URL_TO_PROJECT.split('/') if segment])
SEGMENTS_TO_SERVICE = SEGMENTS_BEFORE_PROJECT_ROOT + 3  # /data/v1/<service-name>/

# Makes Pillow work more reliable with images from the web
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


#######################################################
# INTEGRATION BOOTSTRAP
#######################################################

GOOGLE_CX = environment.datascope.google_cx
GOOGLE_API_KEY = environment.datascope.google_api_key

WIKI_USER = environment.datascope.wiki_user
WIKI_PASSWORD = environment.datascope.wiki_password


#######################################################
# DATAGROWTH BOOTSTRAP
#######################################################

DATAGROWTH_DATA_DIR = os.environ.get('DATAGROWTH_DATA_DIR', os.path.join("..", "data"))


#######################################################
# DJANGO SETTINGS
#######################################################

# Django SECRET_KEY
# Documentation: https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-SECRET_KEY
SECRET_KEY = environment.django.secret_key

DEBUG = environment.django.debug
DEBUG_TOOLBAR = DEBUG

MAX_BATCH_SIZE = 1000
PATH_TO_LOGS = os.path.join(BASE_DIR, "datascope", "logs")

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    # 3rd party
    'django_celery_results',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    # Main app
    'datascope',
    # Framework apps
    'datagrowth',
    'core',
    'sources',
    # Algorithms
    'wiki_feed',
    'visual_translations',
    'future_fashion',
    'open_data',
    'wiki_scope',
    'online_discourse',
    'nautilus',
    'setup_utrecht'
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'datascope',
        'USER': environment.django.database_user,
        'PASSWORD': environment.django.database_password,
        'HOST': environment.postgres.host,
        #'PORT': os.environ.get('PGPORT', '5432')
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    '.localhost',
    '.globe-scope.com',
    '.globe-scope.org',
    '.globe-scope.info',
    '.data-scope.com',
    '.data-scope.org',
    '.data-scope.info',
    '.tools.wmflabs.org',
    '37.139.16.242',
    'ec2-34-251-167-142.eu-west-1.compute.amazonaws.com',
    '.2ndhandstylist.com',
]
CORS_ORIGIN_WHITELIST = [
    'localhost:9000',
    '127.0.0.1:9000',
    '10.0.2.2:9000',
    'localhost:8080',
    '127.0.0.1:8080',
    '10.0.2.2:8080',
    'data-scope.com',
    'www.data-scope.com',
    'globe-scope.com',
    'www.globe-scope.com',
    'debatkijker.nl',
    'www.debatkijker.nl',
    '2ndhandstylist.com',
    'www.2ndhandstylist.com',
]

# Do not redirect when slashes at the end are missing
# Can probably be enabled again if we rewrite paths when upgrading to Django 2.2
APPEND_SLASH = False

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Amsterdam'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False
DATETIME_FORMAT = 'd-m-y H:i:s/u'  # default would get overridden by L18N

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = URL_TO_PROJECT + 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'datascope', 'statics')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_INDEX_FILE = 'index.html'
MEDIA_URL = URL_TO_PROJECT + 'media/'
MEDIA_ROOT = os.path.join(DATAGROWTH_DATA_DIR, "media")

if DEBUG:
    WHITENOISE_USE_FINDERS = True
    WHITENOISE_AUTOREFRESH = True


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'core.templatetags.template_context.core_context',
            ]
        },
    },
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Added for CORS policy (Cross Origin Resource Security)
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Added for serving static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'datascope.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'datascope.wsgi.application'

FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'core', 'tests', 'fixtures'),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s in %(module)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(PATH_TO_LOGS, 'datascope.log'),
            'when': 'midnight',
            'backupCount': 10,
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'datascope': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'datagrowth.command': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        }
    }
}

TEST_RUNNER = "core.tests.runner.DataScopeDiscoverRunner"

SESSION_COOKIE_PATH = '/admin/'

REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

# Celery settings
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = "django-db"
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERYD_TASK_TIME_LIMIT = 300  # 5 minutes for a single task

EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_SUBJECT_PREFIX = "[datascope] "
SERVER_EMAIL = "no-reply@fakoberkers.nl"

#######################################################
# PLUGIN SETTINGS
#######################################################

if USE_WEBSOCKETS:
    INSTALLED_APPS += (
        'ws4redis',
    )
    TEMPLATES[0]["OPTIONS"]["context_processors"].append('ws4redis.context_processors.default')
    WEBSOCKET_URL = '/ws/'
    WS4REDIS_PREFIX = 'ws'
    WSGI_APPLICATION = 'ws4redis.django_runserver.application'
    WS4REDIS_EXPIRE = 0
    WS4REDIS_HEARTBEAT = '--heartbeat--'


# Debug toolbar
# https://django-debug-toolbar.readthedocs.io/en/latest/index.html

if DEBUG_TOOLBAR:
    # Activation
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    MIDDLEWARE = MIDDLEWARE[0:3] + ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE[3:]

    # Configuration
    INTERNAL_IPS = [
        '127.0.0.1',
        'localhost:8000',
    ]
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG
    }


# Elastic Search
# https://elasticsearch-py.readthedocs.io/en/master/

ELASTIC_SEARCH_ANALYSERS = {
    'en': 'english',
    'nl': 'dutch'
}


# Sentry error reporting
# https://sentry.io

if not DEBUG:
    sentry_sdk.init(
        dsn="https://407d0ac6dc4542c9a60fb299e32e464d@sentry.io/241870",
        integrations=[DjangoIntegration()],
        release=DATASCOPE_VERSION,
        server_name='data-scope.com'
    )
