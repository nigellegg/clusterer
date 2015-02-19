# -*- coding: utf-8 -*-
# getdata forms
# copyright 2014 Chibwe Ltd

from django import forms
from django.core.exceptions import ValidationError


class setupForm(forms.Form):
    spreadname = forms.FileField(
        label='Spreadsheet to upload')
    spreadnote = forms.CharField(
        label="Note")
    datcol = forms.CharField(
        label='Data column to cluster')
    clustcol = forms.CharField(
        label='Column for cluster label')
