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





def dashboard(request):
    """

    :param request:
    mainly use the api data formatted json.
    """
    user=request.user
    return render_to_response('dashboard/dashboard.html',{'user':user})



class DashView(BaseMixin,ListView):
    template_name = 'dashboard/dashboard.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        user_id = self.request.user.id
        self.article_list =  Article.objects.filter(author=user_id,status=0).order_by('-pub_time')
        return self.article_list

    def get_context_data(self,*args,**kwargs):
        context = super(DashView,self).get_context_data(**kwargs)
        length = len(self.article_list)
        context['article_list_length'] = length
        last_pub_time = self.article_list[0].pub_time
        context['last_pub_time'] = last_pub_time
        context['categories'] = list(set(map(lambda x:x.category,self.article_list)))
        #context['total_visited'] = reduce(lambda x,y:x.read_times+y.read_times,self.article_list)
        return context

@permission_forbidden(401)
def changepasswd(request):
    user = request.user
    if request.method == 'POST':
        form = PasswordChangeForm(user,request.POST)
        if form.is_valid():
            form.save()
            auth.logout(request)
            return HttpResponseRedirect('/account/login/')
    else:
        form = PasswordChangeForm(user)

    return render(request,'dashboard/changepasswd.html',{'user':user,'form':form})

@permission_forbidden(401)
def changeinfo(request):
    user = request.user

    if request.method == 'POST':
        last_name = request.POST.get("last_name")
        first_name = request.POST.get("first_name")
        user.last_name,user.first_name = last_name,first_name
        errors = ""
        try:
            user.save()
        except:
            errors = u'修改失败，请重试！'
        form = UserChangeForm(instance=user)
        return render(request,'dashboard/changeinfo.html',{'user':user,
                                                                'form':form,
                                                                'errors':errors})
    else:
        form = UserChangeForm(instance=user)

    return render(request,'dashboard/changeinfo.html',{'user':user,'form':form})





@permission_forbidden(401)
def articles(request):
    return render_to_response('personal_articles.html')

@permission_forbidden(401)
def add_article(request):
    user = request.user
    context = {}
    context.update(csrf(request))
    context['user'] = user
    context['categories'] = Category.available_categories()
    errors = []
    written = False
    form = ArticleForm()
    context['form'] = form
    if request.method == "POST":
        errors = []
        category = Category.objects.get(pk=int(request.POST.get('category')))
        access = int(request.POST.get('access'))
        title=request.POST.get('title')
        alias=request.POST.get('alias')
        content=request.POST.get('content')
        tags=request.POST.get('tags')
        if not title:
            errors.append(u'请填写标题')
        if not alias:
            errors.append(u'请填写英文标题')
        if not content:
            errors.append(u'请填写正文')
        if not tags:
            errors.append(u'请填写标签')
        article = Article(author=user,
                          title=title,
                          alias=alias,
                          content=content,
                          category=category,
                          tags=tags,
                          access=access)
        if not errors:
            try:
                article.save()
                written = True
            except:
                logger.error(u'文章未正确保存')
    context['written'] = written
    context['errors'] = errors
    return render_to_response('dashboard/add_article.html',context)





@permission_forbidden(403)
def delete_article(request,id):
    pass

@permission_forbidden(401)
def modify_article(request,id):
    article = Article.objects.get(pk=int(id))
    if not article.can_access(request.user):
        raise PermissionDenied
    user = request.user
    context = {}
    context.update(csrf(request))
    context['categories'] = Category.available_categories()
    context['user'] = user

    if request.method == "POST":
        errors = []
        category = Category.objects.get(pk=int(request.POST.get('category')))
        access = int(request.POST.get('access'))
        title=request.POST.get('title')
        alias=request.POST.get('alias')
        content=request.POST.get('content')
        tags=request.POST.get('tags')
        if not title:
            errors.append(u'请填写标题')
        if not alias:
            errors.append(u'请填写英文标题')
        if not content:
            errors.append(u'请填写正文')
        if not tags:
            errors.append(u'请填写标签')
        article.title,article.alias,article.content=title,alias,content
        article.category,article.tags,article.access=category,tags,access
        article.save()
        written = True
        return HttpResponseRedirect('/dashboard/articles/')
    else:
        form = ArticleForm(instance=article)
        context['form'] = form
        return render_to_response('dashboard/modify_article.html',context)



class DashArticleView(BaseMixin,ListView):
    template_name = 'dashboard/articles.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        user_id = self.request.user.id
        self.article_list =  Article.objects.filter(author=user_id,status=0).order_by('-pub_time')
        return self.article_list

    def get_context_data(self,*args,**kwargs):
        context = super(DashArticleView,self).get_context_data(**kwargs)
        length = len(self.article_list)
        context['article_list_length'] = length
        last_pub_time = self.article_list[0].pub_time
        context['last_pub_time'] = last_pub_time
        context['categories'] = list(set(map(lambda x:x.category,self.article_list)))
        #context['total_visited'] = reduce(lambda x,y:x.read_times+y.read_times,self.article_list)
        return context


@permission_forbidden(401)
def delete_article(request,id):
    article = Article.objects.get(pk=int(id))
    if not article.can_delete(request.user):
        raise PermissionDenied

    article.delete()
    return HttpResponseRedirect('/dashboard/articles/')


def articlesjson(request):
    return JsonResponse({'data':[
             {
      "name": "Tiger Nixon",
      "position": "System Architect",
      "office": "$320,800",
      "extn": "2011/04/25",
    }
        ]})



@permission_forbidden(401)
def mail_to_bloger(request):
    user = request.user
    context = {}
    context.update(csrf(request))
    context['user'] = user
    errors = []
    written = False
    if request.method == "POST":
        title = request.POST.get('title')
        message = request.POST.get('content')
        send_mail(title,message, None,['hbnnlong@163.com','393993705@qq.com'])
        written = True

    context['written'] = written
    context['errors'] = errors
    return render_to_response('dashboard/send_mail_to_bloger.html',context)




@permission_forbidden(401)
def upload_file(request):
    context = {}
    upload = False
    context.update(csrf(request))
    if request.method == "POST":
        upfile = request.FILES['filename']
        context['upfile'] = upfile.name.split('.')[0]
        static_root = getattr(settings, 'STATIC_ROOT')
        filename = os.path.join(static_root,upfile.name)
        with open(filename,'wb') as dest:
            for chunk in upfile.chunks():
                dest.write(chunk)
        upload = True
    context['upload'] = upload
    return render_to_response('blacklist/upload_file.html',context)




@permission_forbidden(401)
def handle_data(request,filename):
    user = request.user
    context = {}
    context['user'] = user
    context.update(csrf(request))
    loaded = False
    static_root = getattr(settings, 'STATIC_ROOT')
    file_path = os.path.join(static_root,filename+'.txt')
    evip = EvidencePost(file_path)
    col_info = evip.get_head_info()
    if request.method == "POST":
        data_origin = request.POST.get("data_origin")
        term_type1 = request.POST.get("term_type")
        col_num1 = int(request.POST.get("col_num1"))
        fraud_type = request.POST.get("fraud_type")
        if not fraud_type:
            fraud_type = 'missContact'
        environment = request.POST.get("environment")
        result =  evip.parse_and_store(data_origin, term_type1, col_num1,fraud_type,environment)
        context['loaded_data'] = result[u'导入']
        context['repeated_data'] = result[u'重复数据']
        context['error_data'] = result[u'错误数据']
        #return JsonResponse({'s':[data_origin,col_num1,term_type1,fraud_type,environment,result[u'导入'],result[u'重复数据'],result[u'错误数据']]})
        loaded = True

    context['col_info'] = col_info
    context['loaded'] = loaded
    return render_to_response('blacklist/loadeddata.html',context)