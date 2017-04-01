import os

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

ALLOWED_HOSTS = ['*']

# Application definition
DJANGO_PROD_APPS = [
]
THIRD_PARTY_PROD_APPS = [
]
LOCAL_PROD_APPS = [
]
INSTALLED_APPS += DJANGO_PROD_APPS + THIRD_PARTY_PROD_APPS + LOCAL_PROD_APPS

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['POSTGRES_DB_NAME'],
        'USER': os.environ['POSTGRES_DB_USER'],
        'PASSWORD': os.environ['POSTGRES_DB_PASSWORD'],
        'HOST': os.environ['POSTGRES_DB_HOST'],
        'PORT': os.environ['POSTGRES_DB_PORT'],
    }
}

# celery config
BROKER_URL = 'amqp://{0}:{1}@{2}:{3}//'.format(os.environ['RABBIT_MQ_USER'],
                                               os.environ['RABBIT_MQ_PASSWORD'],
                                               os.environ['RABBIT_MQ_HOST'],
                                               os.environ['RABBIT_MQ_PORT'],)
# BROKER_URL = 'django://'

CELERY_DEFAULT_QUEUE = 'celery_default_queue'
CMSPYDER_DISCOVER_DOMAINS_QUEUE = 'cmspyder_discover_domains_queue'
CMSPYDER_DETECT_CMS_QUEUE = 'cmspyder_detect_cms_queue'
CELERY_QUEUES = {
    CMSPYDER_DISCOVER_DOMAINS_QUEUE: {
        'exchange': CMSPYDER_DISCOVER_DOMAINS_QUEUE,
        'binding_key': CMSPYDER_DISCOVER_DOMAINS_QUEUE,
    },
    CELERY_DEFAULT_QUEUE: {
        'exchange': CELERY_DEFAULT_QUEUE,
        'binding_key': CELERY_DEFAULT_QUEUE,
    }
}
CELERY_ROUTES = {'spyder.tasks.discover_domains': {'queue': CMSPYDER_DISCOVER_DOMAINS_QUEUE},
                 'spyder.tasks.detect_cms': {'queue': CMSPYDER_DETECT_CMS_QUEUE}}

CELERY_IGNORE_RESULT = True
# CELERY_RESULT_BACKEND = 'amqp'

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# https://celery.readthedocs.io/en/latest/userguide/configuration.html

# maximum number of tasks a pool worker process can execute before it's replaced with a new one,
# to release workers who cause memory leaks
CELERYD_MAX_TASKS_PER_CHILD = 100
# task hard time limit in second
CELERYD_TASK_TIME_LIMIT = 60
# maximum amount of resident memory, in KiB, that may be consumed by a child process before it will
# be replaced by a new one
CELERYD_MAX_MEMORY_PER_CHILD = 50000  # 50 MB
