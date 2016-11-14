"""
WSGI config for cmspyder project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# todo use prod settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cmspyder.settings.dev")

application = get_wsgi_application()
