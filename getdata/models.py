# -*- coding: utf-8 -*-
# getdata models
# copyright 2014 Chibwe Ltd

from django.db import models
from django.core.files.storage import default_storage as s3_storage
from django.contrib.auth.models import User


class Setup(models.Model):
    spreadname = models.FileField(storage=s3_storage, upload_to='cluster/')
    spreadnote = models.CharField(max_length=200)
    datcol = models.CharField(max_length=20)
    clustcol = models.CharField(max_length=20)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.spreadnote
