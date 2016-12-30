#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
from django.views.generic import DetailView,ListView
from django.db.models import Q
import logging
from django.http import Http404
from dailyblog.settings import NUM_PER_PAGE,DOMAIN,SECRET_KEY
import base64
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import auth
from django.db.models import F,Q
from django import forms
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.core.cache import caches
from django.core.mail import send_mail
from django.contrib.auth.models import User
from utils.permissions import permission_forbidden
from utils.get_real_ip import get_real_ip
from utils.jsonify import jsonify
from .forms import UserLoginForm,CustomUserCreationForm
from .models import Article,Category
from utils.token import Token
from resources.logion import get_logion
import random
from django.utils.decorators import method_decorator
from .serializer import CategorySerializer,ArticleSerializer,UserSerializer
import django_filters
from rest_framework import viewsets,filters
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import detail_route
from django.views.generic import View
from blog.views import BaseMixin
from django.http import JsonResponse
import datetime



def uidarticles(request):
    uid = request.user.id
    article_list =  Article.objects.filter(author=uid,status=0).order_by('pub_time')
    xAxis = ['2016-01', '2016-02', '2016-03', '2016-04', '2016-05',
             '2016-06','2016-07', '2016-08', '2016-09', '2016-10', '2016-11', '2016-12']
    months = list(set(map(lambda x:x.pub_time.strftime('%Y-%m'),article_list)))
    count =[]
    for month in xAxis:
        if month not in months:
            count.append(0)
            continue
        single_month_data = filter(lambda x:x.pub_time.strftime('%Y-%m')==month,article_list)
        sum = len(single_month_data)
        count.append(sum)
    current_month = datetime.date.today().strftime('%Y-%m')

    return JsonResponse({'months':xAxis,'count':count})



