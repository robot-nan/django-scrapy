"""
WSGI config for super_worm project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "super_worm.settings")

application = get_wsgi_application()
# gunicorn super_worm.wsgi:application -w 4 -b 127.0.0.1:8000 -k gevent --max-requests 500