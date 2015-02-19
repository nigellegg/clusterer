# -*- coding: utf-8 -*-
# usedata urls
# copyright 2014 Chibwe Ltd

from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView, TemplateView


urlpatterns = patterns('usedata.views',
    url(r'^results/', 'runcluster', name='results'),
    url(r'^nofile/', 'nofile', name='nofile'),
    url(r'^nosheet/', 'nosheet', name='nosheet'),
)
