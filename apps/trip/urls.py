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
from .views import TripIndexView
from utils.permissions import permission_forbidden


router = routers.DefaultRouter()




urlpatterns = [
        url(r'^$',TripIndexView.as_view(),name='tripindex-view'),

]



