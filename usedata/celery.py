# -*-coding: utf-8 -*-
# usedata celery settings
# copyright 2014 Chibwe Ltd

from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clusterer.settings')

app = Celery('usedata')
app.config_from_object('django.conf.settings')
app.autodiscover_tasks(settings.INSTALLED_APPS, related_name='tasks')


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

