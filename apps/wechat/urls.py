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


from django.conf.urls import url,include
from utils.permissions import permission_forbidden
from .views import WechatView,WeArticleListView





urlpatterns = [
    url(r'^hbnnforever/',WechatView.as_view(),name='wechat_public_auth'),
    url(r'^article/list/$',WeArticleListView.as_view(),name='wechat_article_list'),
    url(r'^(?P<id>\w+)/copy/', 'apps.wechat.views.we_article_2_blog', name='copy_article'),

]



