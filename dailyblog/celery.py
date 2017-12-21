from __future__ import absolute_import,unicode_literals

__author__ = 'haibo'
#-*- coding:utf-8 -*-

import os
from celery import Celery, platforms
from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE","dailyblog.settings")


app = Celery('dailyblog')

platforms.C_FORCE_ROOT = True 

app.config_from_object('django.conf:settings')

app.autodiscover_tasks(lambda :settings.INSTALLED_APPS)



