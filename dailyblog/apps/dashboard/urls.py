# -*- coding: utf-8 -*-

"""
    Usage:
            domain/api/articles/
            domain/api/articles/{pk/
            domian/api/articles/author=some_id/
            domain/api/articles/category=some_id/

    Copyright (c):2017 Haibo Wang.
"""


from rest_framework import routers
from django.conf.urls import url,include
from .views import CreateArticleView,UpdateArticleView,DashArticleView,DashView


from utils.permissions import permission_forbidden


router = routers.DefaultRouter()





urlpatterns = [
        url(r'^$',permission_forbidden(401)(DashView.as_view()),name='dashboard'),
        #url(r'^wechat/$',permission_forbidden(401)(WeArticleView.as_view()),name='wechatdashboard'),
        url(r'^articles/$',permission_forbidden(401)(DashArticleView.as_view()),name='dashboardarticles'),
        url(r'^article/add/$',permission_forbidden(401)(CreateArticleView.as_view()),name='add_article'),
        url(r'^article/(?P<pk>\d+)/change/',permission_forbidden(401)(UpdateArticleView.as_view()),name='modify_article'),
        url(r'^article/(?P<pk>\d+)/delete/','apps.dashboard.views.delete_article',name='delete_article'),
        url(r'^wechat/(?P<id>\w+)/copy/','apps.dashboard.views.copy_article',name='copy_article'),
        url(r'^load_online_article/(?P<category>\w+)/','apps.dashboard.views.load_online_article',name='load_online_article'),
        url(r'^uidarticles/$', 'apps.blog.api.uidarticles', name='uidarticles'),
        url(r'^certainarticle/$', 'apps.blog.api.certainarticle', name='certain-article'),
        url(r'^articlelist', 'apps.blog.api.articlelist', name='articlelist'),
       ]



