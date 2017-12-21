#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Usage:
            domain/api/articles/
            domain/api/articles/{pk/
            domian/api/articles/author=some_id/
            domain/api/articles/category=some_id/

    Copyright (c):2016 Haibo Wang.
"""


from rest_framework import routers
from django.conf.urls import url,include
from .views import JobView
from utils.permissions import permission_forbidden


router = routers.DefaultRouter()




urlpatterns = [
        url(r'^$',permission_forbidden(401)(JobView.as_view()),name='job-app-informations'),
        url(r'^display/$','apps.blog.api.jobdisplay',name='job-api-display'),
        url(r'^list/$','apps.blog.api.joblist',name='job-api-list'),
]



