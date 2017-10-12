# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import json
import datetime
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import DetailView,ListView,FormView,CreateView,UpdateView
from django.db.models import Q
import logging
from dailyblog.settings import NUM_PER_PAGE,DOMAIN,SECRET_KEY
import base64
from django.core.exceptions import PermissionDenied
from django.core.cache import caches
from utils.permissions import permission_forbidden
from utils.token import Token
from ..blog.views import BaseMixin
#from utils.resources.wechat.WechatArticle import Wechat_Spider
from utils.papercode import PaperCode
#from utils.resources.weiborobot.weier import Robot
from ..blog.tasks import add_trip,change_img
from ..blog.models import Article,WeArticle,OnlineArticle,Category
from ..blog.forms import ArticleForm


logger = logging.getLogger(__name__)


cache = caches['memcache']



token_confirm = Token(SECRET_KEY)



class DashView(BaseMixin,ListView):
    """
    the index page for dashboard.
    provides author information,including articles,last_login time,and so on.
    """

    template_name = 'dashboard/dashboard.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        user_id = self.request.user.id
        self.article_list =  Article.objects.filter(author=user_id,status=0).order_by('-pub_time')
        return self.article_list

    def get_context_data(self,*args,**kwargs):
        context = super(DashView,self).get_context_data(**kwargs)
        length = len(self.article_list)
        #if user is first registerd,he has no article.
        if length > 0:
            context['article_list_length'] = length
            last_pub_time = self.article_list[0].pub_time
            context['last_pub_time'] = last_pub_time
            context['user_article_categories'] = list(set(map(lambda x:x.category,self.article_list)))
            #context['total_visited'] = reduce(lambda x,y:x.read_times+y.read_times,self.article_list)
        return context


class ArticleMinxin(BaseMixin):
    """
    the Minxin provides categories,they are useful for some palces,such as ,add modify,article.
    """

    def get_context_data(self,*args,**kwargs):
        context = super(ArticleMinxin,self).get_context_data(*args,**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CreateArticleView(ArticleMinxin,CreateView):
    form_class = ArticleForm
    template_name = 'dashboard/add_article.html'
    success_url = '/dashboard/'
    model = Article

    def form_valid(self, form):
        trip_info = form.form_save(self.request)
        if trip_info:
            article_url, title, img, abstract, trip_date = trip_info
            add_trip.delay(article_url, title, img, abstract, trip_date)

        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        return super(CreateArticleView,self).form_invalid(form)



class UpdateArticleView(UpdateView):
    """
    Use UpdateView,I wanna get object.

    """
    form_class = ArticleForm
    template_name = 'dashboard/modify_article.html'
    success_url = '/dashboard/'
    model = Article
    context_object_name = 'article'

    def form_valid(self, form):
        """
        because the article has existed ,it means that,if the article
        belongs to trip,it has created Trip when it is created.
        """
        trip_info = form.form_save(self.request,add=False,object=self.object)
        return HttpResponseRedirect(self.success_url)


    def form_invalid(self, form):
        return super(UpdateArticleView,self).form_invalid(form)



@permission_forbidden(401)
def delete_article(request,pk):
    article = Article.objects.get(pk=int(pk))
    if not article.can_delete(request.user):
        raise PermissionDenied

    article.delete()
    return HttpResponseRedirect('/dashboard/articles/')





class DashArticleView(BaseMixin,ListView):
    """
    you can modify and delete article in this page.
    it provides one table containing all articles you wrote yourselef.

    """
    template_name = 'dashboard/articles.html'
    context_object_name = 'article_list'
    paginate_by = NUM_PER_PAGE

    def get_queryset(self):
        user_id = self.request.user.id
        self.article_list =  Article.objects.defer('content','content_html').filter(author=user_id,status=0).order_by('-pub_time')
        return self.article_list

    def get_context_data(self,*args,**kwargs):
        context = super(DashArticleView,self).get_context_data(**kwargs)
        length = len(self.article_list)
        context['article_list_length'] = length
        last_pub_time = self.article_list[0].pub_time
        context['last_pub_time'] = last_pub_time
        context['display_page_range'] = range(-3,4)
        context['categories'] = list(set(map(lambda x:x.category,self.article_list)))
        #context['total_visited'] = reduce(lambda x,y:x.read_times+y.read_times,self.article_list)
        return context



class WeArticleView(BaseMixin,ListView):
    template_name = 'dashboard/wechat_articles.html'
    context_object_name = 'wechat_article_list'

    def get_queryset(self):
        user_id = self.request.user.id
        self.article_list =  WeArticle.objects.filter(finish=0).order_by('-create_time')
        return self.article_list

    def get_context_data(self,*args,**kwargs):
        context = super(WeArticleView,self).get_context_data(**kwargs)
        return context























@permission_forbidden(401)
def copy_article(request,id):
    wechat_article = WeArticle.objects.get(pk=int(id))
    user = request.user
    category = Category.objects.get(pk=int(19))
    access = int(100)
    title = wechat_article.title
    alias = 'wechat'+str(id)
    try:
        wespider = Wechat_Spider('wechat','Host')
        wearticle = wespider.parse(wechat_article.url)
    except Exception,e:
        return HttpResponse(u'文章爬取出现问题:'+str(e))
    try:
        article = Article(author=user,
                      title=title,
                      alias=alias,
                      content=wearticle['content'],
                      content_html=wearticle['content'],
                      category=category,
                      tags=wearticle['postuser'],
                      abstract= wearticle['abstract'],
                      access=access)
        article.wechat_save()
        wechat_article.finish = 1
        wechat_article.save()
        return HttpResponseRedirect('/dashboard/wechat/')
    except:
        return HttpResponse('save failure')


def weibo(request):
    robot = Robot()
    try:
        robot.send_historyofToday()
        return HttpResponse('Send Success')
    except Exception,e:
        return HttpResponse(str(e))


@permission_forbidden(403)
def load_online_article(request,category=None):
    articles = OnlineArticle.get_latest_articles(category)
    user = request.user
    category_cls = Category.objects.get(name=category)
    if not articles:
        return HttpResponse(u'%s无最新文章'%category)

    for article in articles:
        try:
            blog_article = Article(author=user,
                          title=article['title'],
                          alias=category+unicode(str(article['id'])),
                          content=article['content'],
                          content_html=article['content'],
                          category=category_cls,
                          tags=category_cls.name,
                          abstract=article['author_info']
                          )
            blog_article.wechat_save()
            online_article = OnlineArticle.objects.get(title=article['title'])
            online_article.finish = 1
            online_article.save()
        except Exception,e:
            #return HttpResponse(str(e))
            continue
    return HttpResponseRedirect('/')



