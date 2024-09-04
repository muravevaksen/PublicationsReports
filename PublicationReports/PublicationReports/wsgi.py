"""
WSGI config for PublicationReports project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "'DJANGO_SETTINGS_MODULE', 'PublicationReports.settings'")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"