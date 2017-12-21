# -*- coding: utf-8 -*-

#from __future__ import unicode_literals
import logging

from django.shortcuts import render_to_response
from django.views.generic import DetailView,ListView
from django.http import Http404

from dailyblog.settings import NUM_PER_PAGE,SECRET_KEY

from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from .models import Article,Category
from ..trip.models import Trip
from utils.token import Token
from django.template.context_processors import csrf
from utils.papercode import PaperCode
from utils.cache import Cache
from .tasks import incr_readtimes
from utils.logion import get_logion


logger = logging.getLogger(__name__)




cache = Cache()


token_confirm = Token(SECRET_KEY)


class BaseMixin(object):

    def get_context_data(self,*args,**kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        try:
            context['website_title'] = u'千与千寻'
            context['logion'] = get_logion()
            context['display_page_range'] = range(-3, 4)
            context['carousel_page_list'] = Trip.objects.all()[0:5]
            context['online_ips'] = len(cache.get('onlines'))

        except Exception:
            logger.error('load inital context fails')

        return context


class IndexView(BaseMixin,ListView):
    template_name = 'index.html'
    paginate_by = NUM_PER_PAGE
    context_object_name = 'article_list'

    def get_queryset(self):
        self.keyword = self.request.GET.get('keyword')
        if not self.keyword:
            self.article_list =  Article.get_hottest_articles(number=15)
        else:
            query_sql =( Q(title__icontains=self.keyword) | Q(content__icontains=self.keyword))
            self.article_list = Article.objects.defer('content','content_html').filter(query_sql,status=0)
        return self.article_list

    def get_context_data(self,*args,**kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        context['latest_articles'] =  Article.get_latest_articles()
        return context




class ArticleDetailView(BaseMixin,DetailView):
    queryset = Article.objects.filter(status=0)
    slug_field = 'alias'
    context_object_name = 'article'
    template_name = 'article.html'
    object = None

    def get(self, request, *args, **kwargs):
        alias = self.kwargs.get('slug')
        try:
            self.object = self.queryset.get(alias=alias)
        except Article.DoesNotExist:
            logger.error('article does not exsists')
            #I should rewrite the 404 html later
            return Http404
        # add permission,if the article has set permission,the web will raise one exveption
        if not self.object.can_access(request.user):
            raise PermissionDenied
        #Here,it should be set cache,which store the visited IP
        #Article.objects.filter(id=self.object.id).update(read_times=F('read_times')+1)
        incr_readtimes.delay(self.object.id)
        #If the article's qrcode is 0,generate and add qrcode_url into db:blog_article
        if self.object.qrcode == 0:
            qrcode = PaperCode()
            qrcode_url = qrcode.store_qrcode(self.object.alias)
            self.object.qrcode_url = qrcode_url
            Article.objects.filter(id=self.object.id).update(qrcode=1)
            Article.objects.filter(id=self.object.id).update(qrcode_url=qrcode_url)
        context = self.get_context_data(article=self.object)
        #context['visited_ips'] = len(visited_ips)
        return self.render_to_response(context)


    def get_context_data(self,**kwargs):
        context = super(ArticleDetailView,self).get_context_data(**kwargs)
        context['view_article_title'] = 'show detail article'
        return context



class CategoryArticleListView(BaseMixin,ListView):
    template_name = 'category.html'
    paginate_by = NUM_PER_PAGE
    context_object_name = 'article_list'

    def get_queryset(self):
        alias = self.kwargs.get('alias')
        try:
            self.category = Category.objects.get(alias=alias)
        except Category.DoesNotExist:
            logger.error('no this category')
        article_list = self.category.article_set.all()
        return article_list

    def get_context_data(self,*args,**kwargs):
        kwargs['category_name'] = self.category.name
        return super(CategoryArticleListView,self).get_context_data(**kwargs)



class TagArticleListView(BaseMixin,ListView):
    template_name = 'tag.html'
    paginate_by = NUM_PER_PAGE
    context_object_name = 'article_list'

    def get_queryset(self):
        self.tag = self.kwargs.get('article_tag')
        article_list = Article.objects.defer('content','content_html').filter(tags__icontains=self.tag,status=0)
        return article_list

    def get_context_data(self,*args,**kwargs):
        kwargs['tag_name'] = self.tag
        return super(TagArticleListView,self).get_context_data(**kwargs)




class AuthorView(BaseMixin,ListView):

    template_name = 'author_information.html'
    context_object_name = 'categories'

    def get_queryset(self):
        categories = Category.available_categories()
        return categories

    def get_context_data(self,*args,**kwargs):
        return super(AuthorView,self).get_context_data(**kwargs)





def page_not_found(request):
    return render_to_response('errors/404.html')

def permission_forbidden(request):
    return render_to_response('errors/403.html')

def server_broken(request):
    return render_to_response('errors/500.html')


#@login_required(login_url='/account/login/')
def mail_to_bloger(request):
    user = request.user
    context = {}
    context.update(csrf(request))
    context['user'] = user
    errors = []
    written = False
    if request.method == "POST":
        title = request.POST.get('title')
        title = title if title is not None else u'吐槽你的博客'
        message = request.POST.get('content')
        send_mail(title,message, None,['hbnnlong@163.com','393993705@qq.com'])
        written = True

    context['written'] = written
    context['errors'] = errors
    return render_to_response('advise_to_bloger.html',context)



