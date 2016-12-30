#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    serializer.py
    it is used to create Serializer for Models that created in my project
    Copyright (c) 2016.
"""


from rest_framework import serializers
from .models import  Category,Article
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


class ArticleSerializer(serializers.ModelSerializer):
    #category = CategorySerializer()
    #author = UserSerializer()
    class Meta:
        model = Article
        fields = ('title','content','author','category','pub_time')

