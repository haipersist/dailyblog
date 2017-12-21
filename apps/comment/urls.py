#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

    Copyright (c):2017 Haibo Wang.
"""


from django.conf.urls import url
from .views import CommentListView,CreateCommentView,CommentAuthorView




urlpatterns = [
        url(r'^article/(?P<articleid>\w+)/list/$',CommentListView.as_view(),name='loadcomments'),
        url(r'^article/(?P<articleid>\w+)/create/$',CreateCommentView.as_view(),name='createcomment'),
        url(r'^author/(?P<slug>\w+)/$',CommentAuthorView.as_view(),name='authorcomment'),
        ]



