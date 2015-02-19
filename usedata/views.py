# -*-coding: utf-8 -*-
# usedata views
# copyright 2014 Chibwe Ltd

from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, Context, loader
from django.contrib.auth.decorators import login_required
from getdata.models import Setup
from usedata.tasks import run_clusters
import gspread
import nltk
from nltk.cluster import KMeansClusterer, GAAClusterer
from nltk.cluster import euclidean_distance
import csv
import itertools
import re
from clusterer.settings import TEMP_ROOT
from pusher import Config, Pusher


def runcluster(request):
    pusher = Pusher(app_id='107553',
                    key='6cafdb4abb267445bf93',
                    secret='03da6a0ca85e7e2fcba0')
    pusher[test_channel].trigger('message', {'message': 'Clusterer starting.  You will be sent an emaail when it completes.'})
    setupid = request.session['setup']
    user = request.user
    em_add = user.email
    clustering = run_clusters.delay(setupid, em_add)
    setup = Setup.objects.get(pk=setupid)
    spreadname = setup.spreadname
    datcol = setup.datcol
    clustcol = setup.clustcol
    template = loader.get_template('usedata/results.html')
    context = Context({'spreadname': spreadname, 'datcol': datcol,
                       'clustcol': clustcol})
    return HttpResponse(template.render(context))


def nofile(request):
    setupid = request.session['setup']
    setup = Setup.objects.get(pk=setupid)
    spreadname = setup.spreadname
    template = loader.get_template("usedata/nofile.html")
    context = Context({'spreadname': spreadname})
    return HttpResponse(template.render(context))


def nosheet(request):
    setupid = request.session['setup']
    setup = Setup.objects.get(pk=setupid)
    wsheetname = setup.wsheetname
    spreadname = setup.spreadname
    template = loader.get_template("usedata/nosheet.html")
    context = Context({'spreadname': spreadname, 'wsheetname': wsheetname})
    return HttpResponse(template.render(context))
