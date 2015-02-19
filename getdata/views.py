# -*- coding: utf-8 -*-
# getdata views
# copyright 2014 Chibwe Ltd

from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, Context, loader
from django.contrib.auth.decorators import login_required
from getdata.forms import setupForm
from getdata.models import Setup


def setup(request):
    user = request.user
    if request.method == 'POST':
        form = setupForm(request.POST, request.FILES)
        if form.is_valid():
            newsetup = Setup(spreadname=request.FILES['spreadname'])
            newsetup.spreadnote = form.cleaned_data['spreadnote']
            newsetup.datcol = form.cleaned_data['datcol']
            newsetup.clustcol = form.cleaned_data['clustcol']
            newsetup.user = user
            newsetup.save()
            return HttpResponseRedirect(reverse('getdata.views.setup'))
    else:
        form = setupForm()
    sets = Setup.objects.filter(user=request.user)
    return render(request, 'getdata/setup.html', {'form': form, 'sets': sets})


def confirm(request, Setup_id):
    request.session['setup'] = Setup_id
    setup = Setup.objects.get(pk=Setup_id)
    spreadname = setup.spreadname
    spreadnote = setup.spreadnote
    datcol = setup.datcol
    clustcol = setup.clustcol
    template = loader.get_template('getdata/confirm.html')
    context = Context({'spreadname': spreadname, 'spreadnote': spreadnote,
                       'datcol': datcol, 'clustcol': clustcol})
    return HttpResponse(template.render(context))
