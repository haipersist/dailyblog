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
from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm,PasswordResetForm
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
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes


logger = logging.getLogger(__name__)


try:
    cache = caches['memcache']
except:
    cache = caches['default']

token_confirm = Token(SECRET_KEY)


class BaseMixin(object):

    def get_context_data(self,*args,**kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        try:
            context['website_name'] = u'千与千寻'
            context['categories'] = Category.available_categories()
            context['hottest_articles'] = Article.get_hottest_articles()
            context['latest_articles'] = Article.get_latest_articles()
        except Exception:
            logger.error('load inital context fails')

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
            return HttpResponseNotFound('<h1>Page not Found</h1>')
        # add permission,if the article has set permission,the web will raise one exveption
        if not self.object.can_access(request.user):
            raise PermissionDenied
        #Here,it should be set cache,which store the visited IP
        Article.objects.filter(id=self.object.id).update(read_times=F('read_times')+1)
        ip = get_real_ip(request)
        visited_ips = cache.get(alias,[])
        if ip not in visited_ips:
            visited_ips.append(ip)
            cache.set(alias,visited_ips,60*15)
        context = self.get_context_data(article=self.object)
        context['visited_ips'] = len(visited_ips)
        return self.render_to_response(context)



    def get_context_data(self,**kwargs):
        context = super(ArticleDetailView,self).get_context_data(**kwargs)
        context['view_article_title'] = 'show detail article'
        return context


class IndexView(BaseMixin,ListView):
    template_name = 'index.html'
    paginate_by = NUM_PER_PAGE
    context_object_name = 'article_list'

    def get_queryset(self):
        self.keyword = self.request.GET.get('keyword')
        if not self.keyword:
            self.article_list =  Article.objects.filter(status=0)
        else:
            query_sql =( Q(title__icontains=self.keyword) | Q(content__icontains=self.keyword))
            self.article_list = Article.objects.filter(query_sql,status=0)
        return self.article_list

    def get_context_data(self,*args,**kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)
        length = len(self.article_list)
        context['article_list_length'] = length
        context['keyword'] = self.keyword
        context['logion'] = get_logion()
        number = length if length < 5 else 5
        context['carousel_page_list'] = random.sample(self.article_list,number)
        return context


class CategoryArticleListView(BaseMixin,ListView):
    template_name = 'category.html'
    paginate_by = NUM_PER_PAGE
    context_object_name = 'article_list'

    def get_queryset(self):
        article_list = []
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
        #article_list =[]
        self.tag = self.kwargs.get('article_tag')
        #try:
        article_list = Article.objects.defer('content','content_html').filter(tags__icontains=self.tag,status=0)
        #except Category.DoesNotExist:
        #    logger.error('no this category')
        return article_list

    def get_context_data(self,*args,**kwargs):
        kwargs['tag_name'] = self.tag
        return super(TagArticleListView,self).get_context_data(**kwargs)

@permission_forbidden(http_exception=403)
def TestForm(request):
    if 'start' in request.GET and request.GET['start']:
        return render_to_response('cost.html',{'current':'haibo','start':request.GET['start']})
    else:
        return render_to_response('cost.html',{'current':''})

class AuthorView(BaseMixin,ListView):

    template_name = 'author_information.html'
    context_object_name = 'categories'

    """
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
         return super(AuthorView, self).dispatch(*args, **kwargs)
    """

    def get_queryset(self):
        categories = Category.available_categories()
        return categories

    def get_context_data(self,*args,**kwargs):
        return super(AuthorView,self).get_context_data(**kwargs)




def Login(request):
    errors = []
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username,password = cd['username'],cd['password']
            if not username:
                errors.append(u'请输入用户名')
            if not password:
                errors.append(u'请输入密码')
            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                #this will rewrite html
                return HttpResponseRedirect("/")
            else:
                errors.append(u'无效的用户名或密码，请重新登录。')
        else:
            pass
    else:
        form = UserLoginForm()
    return render(request,'login.html',{'form':form,'errors':errors})


def Register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #new_user = form.save()
            username,password,email = cd['username'],cd['password1'],cd['email']
            user = User.objects.create(username=username, password=password, email=email, is_active=False)
            user.set_password(password)
            user.save()
            token = token_confirm.generate_validate_token(username)
            #active_key = base64.encodestring(username)
            #send email to the register email
            message = "\n".join([
                u'{0},欢迎加入我的博客'.format(username),
                u'请访问该链接，完成用户验证:',
                 '/'.join([DOMAIN,'account/activate',token])
            ])
            send_mail(u'注册用户验证信息',message, None,[cd['email']])
            #user = auth.authenticate(username=username,password=password)
            #auth.login(request,user)
            return HttpResponse(u"请登录到注册邮箱中验证用户，有效期为1个小时。")
    else:
        form = CustomUserCreationForm()
    return render(request,'register.html',{'form':form})

@login_required(login_url='/account/login/')
def Logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='/account/login/')
def Changepassword(request):
    if request.method == 'POST':
        errors = []
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            auth.logout(request)
            return HttpResponseRedirect('/account/login/')
    else:
        form = PasswordChangeForm(request.user)
    return render(request,'changepassword.html',{'form':form})



def forgetpasswd(request):
    sent,note = False,None
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            token_generator = default_token_generator
            for user in form.get_users(email):
                uid =  urlsafe_base64_encode(force_bytes(user.id))
                token = token_generator.make_token(user)
            try:
                message = "\n".join([
                    u'您的用户名是:%s' % user.username,
                    u'请访问该链接，进行密码重置:',
                     '/'.join([DOMAIN,'account/resetpwd',uid,token])+'/',
                ])
            except:
                logger.error(u'请正确填写邮箱')
            send_mail(u'注册用户密码重置',message, None,[email])
            sent = True
        else:
            note = u'请填写正确邮箱！'
    else:
        form = PasswordResetForm()

    context = {
        'form':form,
        'sent':sent,
        'note':note
    }
    return render(request,'forgetpasswd.html',context)


def ResetPasswd(request,uidb64=None, token=None,
                token_generator=default_token_generator,
                set_password_form=SetPasswordForm):

    UserModel = get_user_model()
    assert uidb64 is not None and token is not None
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None
    if user is not None and token_generator.check_token(user, token):
        resettitle = u'输入新密码'
        validlink = True
        if request.method == "POST":
            form = set_password_form(user,request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/account/login/')
        else:
            form = set_password_form(user)
    else:
        validlink = False
        form = None
        resettitle = u'用户不存在'
    context = {
        'form':form,
        'validlink':validlink,
        'resettitle':resettitle
    }
    return render(request,'resetpwd.html',context)



def active_user(request,token):
    """
    the view function is used to accomplish the user register confirm,only after input the link
    that sent to the register email,user can login the site normally.
    :param request:
    :param activate_key:the paragram is gotten by encrypting username when user register
    :return:
    """
    try:
        username = token_confirm.confirm_validate_token(token)
    except:
        return HttpResponse(u'对不起，验证链接已经过期')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse(u'对不起，您所验证的用户不存在，请重新注册')
    user.is_active = True
    user.save()
    confirm = u'验证成功，请进行登录操作。'
    return HttpResponseRedirect('/account/login',{'confirm':confirm})




def ajax_login(request):
    username = request.POST.get('username',None)
    password = request.POST.get('password',None)
    user = auth.authenticate(username=username,password=password)
    errors = []
    if user is not None:
        auth.login(request,user)
    else:
        errors.append(u'用户名或密码不正确')

    return HttpResponse(
        jsonify(errors=errors),
        content_type="application/json"
    )



class CategoryViewset(viewsets.ModelViewSet):
    # ViewSets define the view behavior.
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def perform_create(self, serializer):
        serializer.save()


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer


class ArticleViewset(viewsets.ModelViewSet):
    """
    the viewset let us can get data from api url
    like:curl - H 'application/json;indent=4' http://localhost:8080/api/articles/
    of course,we can get some author's article through:
    http://localhost:8080/api/articles/?author=2(author's id)
    Generally,people like to see json data,so when visit by browser,you should add
    ?format=json ,that is,http://localhost:8080/api/articles/?format=json

    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('author','category','access','status')



def page_not_found(request):
    return render_to_response('errors/404.html')

def permission_forbidden(request):
    return render_to_response('errors/403.html')

def server_broken(request):
    return render_to_response('errors/500.html')