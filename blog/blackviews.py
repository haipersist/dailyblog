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
from django.contrib.auth.forms import PasswordChangeForm,UserChangeForm
from django.contrib import auth
from django.db.models import F,Q
from django import forms
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.core.cache import caches
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
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
from django.utils.encoding import force_bytes
from django.utils.html import format_html, format_html_join
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import RequestContext
from blog.forms import ArticleForm
from django.template.context_processors import csrf
from .resources.StoreData import EvidencePost
from django.conf import settings
import os
logger = logging.getLogger(__name__)


try:
    cache = caches['memcache']
except:
    cache = caches['default']

token_confirm = Token(SECRET_KEY)



def handle_data(request):
    user = request.user
    context = {}
    context['user'] = user
    context.update(csrf(request))
    loaded = False
    if request.method == "POST":
        data_origin = request.POST.get("data_origin")
        term_type1 = request.POST.get("term_type",'accountMobile')
        col_num1 = int(request.POST.get("col_num1"))
        fraud_type = request.POST.get("fraud_type",'missContact')
        environment = request.POST.get("environment")
        static_root = getattr(settings, 'STATIC_ROOT')
        file_path = os.path.join(static_root,'test.txt')
        print data_origin,col_num1,term_type1,fraud_type
        print file_path
        evip = EvidencePost(file_path)
        evip.get_head_info()
        result =  evip.parse_and_store(data_origin, term_type1, col_num1,fraud_type,environment)
        context['loaded_data'] = result[u'导入']
        context['repeated_data'] = result[u'重复数据']
        context['error_data'] = result[u'错误数据']
        loaded = True

    context['loaded'] = loaded
    return render_to_response('blacklist/loadeddata.html',context)


