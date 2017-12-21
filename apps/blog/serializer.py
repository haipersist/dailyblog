#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    serializer.py
    it is used to create Serializer for Models that created in my project
    Copyright (c) 2016.
"""


from rest_framework import serializers
from .models import  Category,Article,OnlineArticle
from ..comment.models import Author,Comment,ReplyComment
from ..dashboard.models import VisitIp,VisitPv,VisitUv
from django.contrib.auth.models import User
from django.forms import widgets

class CategorySerializer(serializers.ModelSerializer):
    # Serializers define the API representation.
    class Meta:
        model = Category
        fields = ('id','name','alias','parent','create_time','status')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','last_login','first_name','last_name')


class OnlineArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineArticle
        fields = ('id','title','content','author_info','category','finish','url','create_time')




class ArticleSerializer(serializers.ModelSerializer):
    #category = CategorySerializer()
    #author = UserSerializer()
    class Meta:
        model = Article
        fields = ('title','content','author','category','pub_time','alias','qrcode_url')


class VisitIpSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitIp

class VisitPvSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitPv

class VisitUvSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitUv

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        pass
        fields = ('id','title','welfare','requirement','link','salary','company','website','pub_time')


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        pass
        fields = ('id','name','address','introduction','homepage')


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('name','email')


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    article = ArticleSerializer()

    class Meta:
        model = Comment
        fields = ('content','article','author','create_time')


class ReplyCommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    comment = CommentSerializer()

    class Meta:
        model = ReplyComment
        fields = ('content','reply_to','author','create_time','comment')



