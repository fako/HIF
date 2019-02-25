import os
import logging


log = logging.getLogger(__name__)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


#######################################################
# DEFAULT BOOTSTRAP
#######################################################

PATH_TO_PROJECT = ''
URL_TO_PROJECT = '/'
USE_WEBSOCKETS = False
SECRET_KEY = 'default'
DATABASE_TYPE = 'postgres'
MYSQL_USER = 'postgres'
MYSQL_PASSWORD = ''
USE_MOCKS = False

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


#######################################################
# LOAD ENVIRONMENT
#######################################################

try:
    from .bootstrap import *
except ImportError:
    log.warning("Could not import bootstrap settings. Are they created?")
try:
    from .secrets import *
except ImportError:
    log.error("Could not import secret settings. Are they created? Do not run in production!")

DATABASE_USER = os.environ.get('DJANGO_DATABASE_USER', MYSQL_USER)
DATABASE_PASSWORD = os.environ.get('DJANGO_DATABASE_PASSWORD', MYSQL_PASSWORD)


#######################################################
# DJANGO SETTINGS
#######################################################

DEBUG = False
DEBUG_TOOLBAR = False

MAX_BATCH_SIZE = 1000
PATH_TO_LOGS = PATH_TO_PROJECT + "datascope/logs/"

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
    'raven.contrib.django.raven_compat',
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
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': '127.0.0.1',
        'PORT': os.environ.get('PGPORT', '5432')
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

# Available languages for all projects
ugettext = lambda s: s  # a dummy ugettext to prevent circular import
LANGUAGES = (
    ('en', ugettext('English')),
    ('pt', ugettext('Portuguese')),
    ('nl', ugettext('Dutch')),
    ('de', ugettext('German')),
    ('es', ugettext('Spanish')),
    ('fr', ugettext('French')),
)

LOCALE_PATHS = (
    PATH_TO_PROJECT + 'src/locale/',
)

SEGMENTS_BEFORE_PROJECT_ROOT = len([segment for segment in URL_TO_PROJECT.split('/') if segment])
SEGMENTS_TO_SERVICE = SEGMENTS_BEFORE_PROJECT_ROOT + 3  # /data/v1/<service-name>/

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'data', 'media', '')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = URL_TO_PROJECT + 'media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = PATH_TO_PROJECT + 'datascope/statics/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = URL_TO_PROJECT + 'static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

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

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Datascope middleware
    'core.middleware.origin.AllowOriginMiddleware',
)

ROOT_URLCONF = 'datascope.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'datascope.wsgi.application'

FIXTURE_DIRS = (
    PATH_TO_PROJECT + 'core/tests/fixtures/',
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
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': PATH_TO_LOGS + 'datascope.log',
            'when': 'midnight',
            'backupCount': 10,
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'sentry'],
            'level': 'ERROR',
            'propagate': True,
        },
        'datascope': {
            'handlers': ['file', 'sentry'],
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
    #'DEFAULT_PAGINATION_CLASS': 'core.views.content.ContentPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
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
