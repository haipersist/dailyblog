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
from .views import CategoryViewset,ArticleViewset,UserViewset
from .dashboard_views import DashView,DashArticleView
from utils.permissions import permission_forbidden


router = routers.DefaultRouter()

router.register(r'categories',CategoryViewset)
router.register(r'articles',ArticleViewset)
router.register(r'users',UserViewset)


urlpatterns = [
        url(r'^$',permission_forbidden(401)(DashView.as_view()),name='dashboard'),
        url(r'^articles/$',permission_forbidden(401)(DashArticleView.as_view()),name='dashboardarticles'),
        url(r'^uidarticles/$','blog.api.uidarticles',name='uidarticles'),
        url(r'^json/$','blog.dashboard_views.articlesjson',name='jsonarticles'),
        url(r'^send_mail/$','blog.dashboard_views.mail_to_bloger',name='mailtobloger'),
        url(r'^profile/$','blog.dashboard_views.changepasswd',name='personalpwd'),
        url(r'^profileinfo/$','blog.dashboard_views.changeinfo',name='personalinfo'),
        url(r'^article/add/$','blog.dashboard_views.add_article',name='add_article'),
        url(r'^article/(?P<id>\w+)/change/','blog.dashboard_views.modify_article',name='modify_article'),
        url(r'^article/(?P<id>\w+)/delete/','blog.dashboard_views.delete_article',name='delete_article'),
        url(r'^loaddata/(?P<filename>\w+)/$','blog.dashboard_views.handle_data',name='handle_data'),
        url(r'^upfile/','blog.dashboard_views.upload_file',name='upload_txtfile'),
]



