"""
WSGI config for Apps4Ghent_Library project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys

path='/var/www/Apps4Ghent_Library'

if path not in sys.path:
	sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Apps4Ghent_Library.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
