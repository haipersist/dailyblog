#!/usr/bin/env python
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
#from django.conf.urls import url,include
from .viewset import CategoryViewset,ArticleViewset,UserViewset,\
        OnlineArticleViewset,VisitIpViewset,JobViewset,CompanyViewset,\
        AuthorCommentViewset,CommentViewset,ReplyCommentViewset


router = routers.DefaultRouter()

router.register(r'categories',CategoryViewset)
router.register(r'articles',ArticleViewset)
router.register(r'users',UserViewset)
router.register(r'onlines',OnlineArticleViewset)
#router.register(r'visitips',VisitIpViewset)
#router.register(r'jobs',JobViewset)
#router.register(r'companies',CompanyViewset)
router.register(r'comments',CommentViewset)
router.register(r'replycomments',ReplyCommentViewset)
router.register(r'comment_author',AuthorCommentViewset)


urlpatterns = [

        ]



