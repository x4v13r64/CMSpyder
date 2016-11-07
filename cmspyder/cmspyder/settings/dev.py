import os

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@-94qf(l2pj7yn7c@$%77vp=jkon#p^@%+_eac&x&o@835(v*q'

ALLOWED_HOSTS = []

# Application definition
DJANGO_DEV_APPS = [
]
THIRD_PARTY_DEV_APPS = [
    'django_nose',
    # 'debug_toolbar',
]
LOCAL_DEV_APPS = [
]
INSTALLED_APPS += DJANGO_DEV_APPS + THIRD_PARTY_DEV_APPS + LOCAL_DEV_APPS

# Application middleware
MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + [
   # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TEMPLATE_CONTEXT': True,
}

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.run_tests'
TEST_OUTPUT_VERBOSE = True
TEST_OUTPUT_DESCRIPTIONS = True
TEST_OUTPUT_DIR = 'xmlrunner'

# celery config
BROKER_URL = 'django://'
CELERY_RESULT_BACKEND = 'amqp'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
