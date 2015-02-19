# -*- coding: utf-8 -*-
# getdata urls
# copyright 2014 Chibwe Ltd

from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView, TemplateView


urlpatterns = patterns('getdata.views',
    url(r'^setup/$', 'setup', name='setup'),
    url(r'^confirm/(?P<Setup_id>\d+)/$', 'confirm', name='confirm'),
    )
