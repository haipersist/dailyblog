# -*- coding: utf-8 -*-

#from __future__ import unicode_literals
import logging
from django.contrib.auth.models import User
from utils.permissions import UserPermisson,ArticlePermisson
from .models import Article,Category,OnlineArticle
from ..comment.models import  Author,Comment,ReplyComment
from .serializer import CategorySerializer,ArticleSerializer,UserSerializer,\
    OnlineArticleSerializer,VisitIpSerializer,VisitPvSerializer,JobSerializer,CompanySerializer,\
    AuthorSerializer,CommentSerializer,ReplyCommentSerializer,VisitUvSerializer
from rest_framework import viewsets,filters
from rest_framework.permissions import IsAdminUser
from utils.cache import Cache
from ..dashboard.models import VisitIp,VisitPv,VisitUv


logger = logging.getLogger(__name__)




cache = Cache()




class CategoryViewset(viewsets.ModelViewSet):
    # ViewSets define the view behavior.
    queryset = Category.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = CategorySerializer
    filter_fields = ('id','alias','name')


class OnlineArticleViewset(viewsets.ModelViewSet):
    # ViewSets define the view behavior.
    queryset = OnlineArticle.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class =OnlineArticleSerializer


class VisitIpViewset(viewsets.ModelViewSet):
    queryset = VisitIp.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class =VisitIpSerializer

class VisitPvViewset(viewsets.ModelViewSet):
    queryset = VisitPv.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class =VisitPvSerializer

class VisitUvViewset(viewsets.ModelViewSet):
    queryset = VisitUv.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = VisitUvSerializer


class JobViewset(viewsets.ModelViewSet):
    # ViewSets define the view behavior.
    #queryset = Job.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = JobSerializer


class CompanyViewset(viewsets.ModelViewSet):
    # ViewSets define the view behavior.
    #queryset = Company.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = CompanySerializer


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer
    #set filter field that display
    filter_fields = ('username','email','date_joined','last_login')



class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_fields = ('article','author','create_time')


class ReplyCommentViewset(viewsets.ModelViewSet):
    queryset = ReplyComment.objects.all()
    serializer_class = ReplyCommentSerializer
    filter_fields = ('comment','author','create_time')

class AuthorCommentViewset(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_fields = ('email')


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
    permission_classes = (ArticlePermisson,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('author','category','access','status')


