from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings  # noqa

# set the default Django settings module for the 'celery' program
# must always appear before the app instance is created
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cmspyder.settings')


app = Celery('cmspyder')

# Add the Django settings module as a configuration source for Celery. This means that you don't
# have to use multiple configuration files, and instead configure Celery directly from the Django
# setting.
app.config_from_object('django.conf:settings')
# enable Celery to autodiscover these modules in tasks.py
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
