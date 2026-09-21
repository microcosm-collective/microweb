"""
WSGI config for microweb project.

It exposes the WSGI callable as a module-level variable named ``application``.
Static files are served by whitenoise, wired in as
``whitenoise.middleware.WhiteNoiseMiddleware`` in settings.
"""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "microweb.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
