"""
WSGI config for RecentCSCSTS project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Determine the settings module based on the environment variable
# If 'WEB_HOSTNAME' is set, use the production settings; otherwise, use the default settings.
settings_module = 'RecentCSCSTS.deployment' if 'WEB_HOSTNAME' in os.environ else 'RecentCSCSTS.settings'

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

application = get_wsgi_application()
