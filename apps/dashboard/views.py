# -*- coding: utf-8 -*-
"""

The dashboard is one content management platform. any user who has been logged in this website

have his dasboard.

In it you can:

      1.Manage every aritlce wrriten by you,modify or delete.
      2.create one article.


"""
from __future__ import unicode_literals
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import DetailView,ListView,FormView,CreateView,UpdateView
import logging
from dailyblog.settings import NUM_PER_PAGE,DOMAIN,SECRET_KEY
import base64
from django.core.exceptions import PermissionDenied
from django.core.cache import caches
from utils.permissions import permission_forbidden
from utils.token import Token
from ..blog.views import BaseMixin

from ..blog.tasks import add_trip
from ..blog.models import Article,OnlineArticle,Category
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
            return HttpResponseRedirect('/')

        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        return super(CreateArticleView,self).form_invalid(form)



class UpdateArticleView(ArticleMinxin,UpdateView):
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



