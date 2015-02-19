# -*- coding: utf-8 -*-
# clusterer wsgi
# copyright 2014 Chibwe Ltd

"""
WSGI config for reuben project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clusterer.settings")

from django.core.wsgi import get_wsgi_application
from dj_static import Cling
application = Cling(get_wsgi_application())
