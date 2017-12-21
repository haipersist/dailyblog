#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime
from models import Article,Category
from ..comment.models import Comment,ReplyComment,Author
from ..job.models import Job
import random
from django.utils.decorators import method_decorator
from .serializer import CategorySerializer,ArticleSerializer,UserSerializer
import django_filters
from rest_framework import viewsets,filters
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import detail_route
from django.views.generic import View,ListView,CreateView,DetailView
from views import BaseMixin
from django.http import JsonResponse
import datetime
import requests
from dailyblog.settings import DOMAIN
from datetime import date
from utils.permissions import permission_forbidden,UserPermisson,ArticlePermisson
from utils.djmodel2dict import djmodel2dict
from utils.token import Token
from utils.get_real_ip import get_real_ip
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from utils.validate_email import ValidateEmail


ArticleApi = '/'.join([DOMAIN,'api/articles/'])
UserApi = '/'.join([DOMAIN,'api/users/'])
CategoryApi = '/'.join([DOMAIN,'api/categories/'])




def uidarticles(request):
    year = str(date.today().year)
    user = request.user
    if user.is_superuser != 1:
        article_list = Article.objects.filter(author=user.id, status=0).order_by('pub_time')
    else:
        article_list = Article.objects.filter(status=0).order_by('pub_time')
    xAxis = []
    for month in range(1,13):
        month  = '0' + str(month)  if month < 10 else str(month)
        xitem = '-'.join([year,month])
        xAxis.append(xitem)
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


@permission_forbidden(403)
def articlelist(request):
    user = request.user
    articles = []
    if user.is_superuser != 1:
        article_list =  Article.objects.filter(author=user.id,status=0).order_by('pub_time')
    else:
        article_list =  Article.objects.filter(status=0).order_by('pub_time')
    for article in article_list:
        item = {}
        item['title'] = u'<a href="/article/'+article.alias+u'.html">'+article.title+u'</a>'
        #item['alias'] = article.alias
        item['author'] = article.author.username
        item['read_times'] = article.read_times
        item['pub_time'] = article.pub_time.strftime('%Y-%m-%d')
        articles.append(item)

    return JsonResponse({'data':articles})


def decorator(articles):
    items = []
    for article in articles:
        item = {}
        item['title'] = article['title']
        item['alias'] = article['alias']
        item['read_times'] = article['read_times']
        items.append(item)
    return items


def certainarticle(request):
    user = request.user
    result = {}
    categories = Category.available_categories()
    items = []
    for category in categories:
        category.id = len(category.article_set.all())
        item = {}
        item['name'] =category.name
        item['alias'] = category.alias
        item['id'] = category.id
        items.append(item)
    result.setdefault('side_categories',items)
    result.setdefault('categories',items)

    hottest, latest_articles = decorator(Article.get_hottest_articles().values()), \
                               decorator(Article.get_latest_articles().values())
    result.setdefault('hottest_articles', hottest)
    result.setdefault('latest_articles', latest_articles)
    return JsonResponse(result)


def dict_decorator(jobs):
    jobdata = []
    for job in jobs:
        result = {}
        result['title'] = job.title
        result['company'] = job.company.name
        result['salary'] = job.salary
        result['website'] = job.website.website
        #job['welfare'] = job.title.strftime('%Y-%m-%d')
        result['pub_time'] = job.load_time.strftime('%Y-%m-%d')
        result['link'] = u'<a href="' + job.link + u'">招聘链接</a>'
        jobdata.append(result)
    return jobdata


def date_decorator(func):
    def wrapper(request):
        start = request.GET.get('start',None)
        end = request.GET.get('end',None)
        if not end:
            end = None
        if not start:
            start = None
        request.GET['start'] = start
        request.GET['end']= end
        return func(request)
    return wrapper


@permission_forbidden(403)
def joblist(request):
    #对于Datetime字段，像下面查询的话，会自动翻译成 between '2017-03-05 00:00:00' AND '2017-03-10 00:00:00'
    start = request.GET.get('start',None)
    end = request.GET.get('end',None)
    if not end:
        end = None
    if not start:
        start = None
    #jobs = Job.get_certain_articles(start=start,end=end)
    jobs = Job.get_certain_jobs(start=start,end=end)
    data = dict_decorator(jobs)
    result = {}
    result.setdefault('data',data)
    return JsonResponse(result)


#@permission_forbidden(401)
def jobdisplay(request):
    start = request.GET.get('start','')
    end = request.GET.get('end','')
    if not end:
        end = None
    if not start:
        start = None
    jobs = Job.get_job_count_by_day(start,end)
    xAxis = [job['pub_time'] for job in jobs]
    count = [job['count'] for job in jobs]
    return JsonResponse({'months':xAxis,'count':count})



