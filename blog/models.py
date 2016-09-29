#!/usr/bin/env python
# -*- coding: utf-8 -*-



from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.functional import cached_property
from datetime import datetime
from dailyblog import settings
from utils.jsonify import jsonify
from markdown import markdown
from utils.cache import Cache

STATUS = {
    0:u'正常',
    1:'草稿',
    2:'删除',
}

ACCESS = {
    100:u'公开',
    200:u'私人可见'
}



class Category(models.Model):

    name = models.CharField(max_length=150,unique=True,verbose_name=u'类名')
    alias = models.CharField(max_length=150,verbose_name=u'英文名称')
    status = models.IntegerField(default=0,choices=STATUS.items(),verbose_name=u'状态')
    #Automatically set the field to now when the object is first created.
    create_time = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self',default=None,blank=True,null=True,verbose_name=u'上级分类')


    def __unicode__(self):
         if self.parent:
             return "{0}:{1}".format(self.parent,self.name)
         else:
             return '%s' % self.name

    @classmethod
    def available_categories(cls):
         return cls.objects.filter(status=0)


    class Meta:
         ordering = ['-create_time']
         verbose_name = u'分类'



mycache = Cache()

class Article(models.Model):

    title = models.CharField(max_length=150,unique=True,verbose_name=u'标题')
    alias = models.CharField(max_length=150,verbose_name=u'英文标题')
    content = models.TextField(verbose_name=u'正文')
    #when editing article,content_html will be saved automatically from content.so it can be blank
    content_html = models.TextField(blank=True,verbose_name=u'正文html格式')
    abstract = models.TextField(blank=True,verbose_name=u'摘要')
    read_times = models.IntegerField(default=0,verbose_name=u'阅读次数')
    tags = models.CharField(max_length=100,verbose_name=u'标签',help_text='用逗号隔开')
    status = models.IntegerField(default=0,choices=STATUS.items(),verbose_name=u'文章状态')
    #Automatically set the field to now when the object is first created
    create_time = models.DateTimeField(auto_now_add=True)
    pub_time = models.DateTimeField(default=datetime.now())
    #Automatically set the field to now every time the object is saved.
    update_time = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User,verbose_name=u'作者')
    category = models.ForeignKey(Category,verbose_name=u'分类')
    access = models.IntegerField(default=100,choices=ACCESS.items(),verbose_name=u'文章权限，公开或者私人可见')


    def __unicode__(self):
        return '%s' % self.title

    def save(self):
        self.content_html = markdown(self.content,output_format='html5')
        self.abstract = self.content[:200]
        super(Article,self).save()

    @property
    def absolute_url(self):
        return '{0}/article/{1}.html'.format(settings.DOMAIN,self.alias)

    @property
    def tag_list(self):
        tag_list = [tag.strip() for tag in self.tags.split(',')]
        return tag_list

    @classmethod
    @mycache.cached(300)
    def get_hottest_articles(cls,number=5):
        return cls.objects.filter(status=0).values('title','alias','read_times').order_by('-read_times')[:number]

    @classmethod
    def get_latest_articles(cls,number=5):
        return cls.objects.filter(status=0).values('title','alias','pub_time').order_by('-pub_time')[:number]

    @cached_property
    def next_article(self):
        # 下一篇
        return Article.objects.filter(id__gt=self.id, status=0).order_by('id').first()

    @cached_property
    def pre_article(self):
        # 前一篇
        return Article.objects.filter(id__lt=self.id, status=0).first()

    def can_access(self,user):
        if self.access == 100:
            return True
        if self.access == 200:
            if user is None:
                return False
            else:
                return self.author.id == user.id or user.is_staff

    def can_delete(self,user):
        return self.author.id == user.id or user.is_staff

    def get_json(self):
        return jsonify(title=title,
                       author=author,
                       tags=tags,
                       category=category,
                       create_time=create_time,
                       status=status,
                       read_times=read_times,
                       )

    class Meta:
        ordering = ['-pub_time','-create_time']
        get_latest_by = 'create_time'
        verbose_name = u'文章'

















