"""
WSGI config for epropertyproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from web.background.processes.validate_posts import ValidateAllPostsThread

os.environ['DJANGO_SETTINGS_MODULE'] = 'eproperty.settings'

application = get_wsgi_application()

ValidateAllPostsThread(10).start()
