# -*- coding: utf-8 -*-
# clusterer urls
# copyright 2014 Chibwe Ltd

from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView, TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^/$', TemplateView.as_view(template_name="home.html"), name="home"),
    url(r'^home/', TemplateView.as_view(template_name="home.html"), name="home"),
    url(r'^getdata/', include('getdata.urls')),
    url(r'^usedata/', include('usedata.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^contact/', TemplateView.as_view(template_name="contact.html"), name="contact"),
    # Examples:
    # url(r'^$', 'reuben.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
