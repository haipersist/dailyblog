#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Usage:


    Copyright (c):2017 Haibo Wang.
"""


from rest_framework import routers
from django.conf.urls import url
from .views import ChangePasswdView,LoginView,RegisterView,ChangeUserprofileView, \
    UserProfileView,ForgetPasswdView,ResetPasswdView
from utils.permissions import permission_forbidden


router = routers.DefaultRouter()



urlpatterns = [
    url(r'^register/$', RegisterView.as_view(), name='register-view'),
    url(r'^login/$',LoginView.as_view(),name='account-login'),
    url(r'^ajax_login/$','apps.account.views.ajax_login',name='ajax_login'),
    url(r'^logout/$','apps.account.views.Logout',name='logout'),
    url(r'^changepassword/$',permission_forbidden(401)(ChangePasswdView.as_view()),name='changepwd-view'),
    url(r'^forgetpasswd/$',ForgetPasswdView.as_view(),name='forgetpasswd'),
    url(r'^resetpwd/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',ResetPasswdView.as_view(),name='resetpassword'),
    url(r'^activate/(?P<token>\w+.\w+.[-_\w]*\w+)/$','apps.account.views.active_user',name='active_user'),
    url(r'^changeuserprofile/$', permission_forbidden(401)(ChangeUserprofileView.as_view()),
        name='change_personal_userprofile'),
    url(r'^userprofile/$', permission_forbidden(401)(UserProfileView.as_view()), name='personal_userprofile'),

]



