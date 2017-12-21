# -*- coding: utf-8 -*-


from __future__ import unicode_literals
import random
from django.db import models
from django.contrib.auth.models import User
from django.utils.functional import cached_property
from datetime import datetime,date,timedelta
from django.conf import settings
from utils.jsonify import jsonify
from markdown import markdown
from utils.cache import Cache
#from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

STATUS = {
    0:'正常',
    1:'草稿',
    2:'删除',
}

ACCESS = {
    100:'公开',
    200:'私人可见'
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
         verbose_name = '文章分类'
         app_label = 'blog'



mycache = Cache()


class Article(models.Model):

    title = models.CharField(max_length=150,unique=True,verbose_name='标题')
    alias = models.CharField(max_length=150,verbose_name='英文标题')
    content = RichTextUploadingField(verbose_name='正文')
    #when editing article,content_html will be saved automatically from content.so it can be blank
    content_html = models.TextField(blank=True,verbose_name='正文html格式')
    abstract = models.TextField(blank=True,verbose_name='摘要')
    read_times = models.IntegerField(default=0,verbose_name='阅读次数')
    tags = models.CharField(max_length=100,verbose_name='标签',help_text='用逗号隔开')
    status = models.IntegerField(default=0,choices=STATUS.items(),verbose_name='文章状态')
    #Automatically set the field to now when the object is first created
    create_time = models.DateTimeField(auto_now_add=True)
    pub_time = models.DateTimeField(auto_now=True)
    #Automatically set the field to now every time the object is saved.
    update_time = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User,verbose_name='作者',blank=True)
    category = models.ForeignKey(Category,verbose_name='分类')
    access = models.IntegerField(default=100,choices=ACCESS.items(),verbose_name='文章权限，公开或者私人可见')
    qrcode = models.IntegerField(default=0,verbose_name='二维码状态')
    qrcode_url = models.CharField(max_length=255,unique=True,verbose_name='二维码链接')


    def __unicode__(self):
        return '%s' % self.title

    def ck_save(self):
        self.content_html = self.content
        super(Article,self).save()

    @property
    def absolute_url(self):
        return '/article/{0}.html'.format(self.alias)

    @classmethod
    def get_url_with_domain(self,alias):
        return settings.DOMAIN + 'article/{0}.html'.format(alias)

    @property
    def tag_list(self):
        sep = ','
        #if has chinese '，',replace it with English
        if '，' in self.tags:
            self.tags = self.tags.replace('，',',')
        tag_list = [tag.strip() for tag in self.tags.split(sep)]
        return tag_list

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

    @classmethod
    @mycache.cached(300)
    def get_hottest_articles(cls,number=8):
        return cls.objects.filter(status=0).defer('content','content_html').order_by('-read_times')[:number]

    @classmethod
    @mycache.cached(300)
    def get_latest_articles(cls,number=8):
        return cls.objects.filter(status=0).defer('content','content_html').order_by('-create_time')[:number]

    @classmethod
    @mycache.cached(300)
    def get_articles_by_cat(cls,categoryId,number=8):
        """
        :param category:{'心情日记':10,'名人作品':26,'Django开发':3}
        :param number:
        :return:
        """
        if not isinstance(categoryId,int):
            categoryId = int(categoryId)
        category = Category.objects.get(pk=categoryId)
        return cls.objects.filter(status=0,category=category) \
                   .values('title','alias','read_times') \
                   .order_by('-read_times')[:number]

    @cached_property
    def next_article(self):
        # 下一篇
        return Article.objects.filter(id__gt=self.id, status=0).order_by('id').first()

    @cached_property
    def pre_article(self):
        # 前一篇
        return Article.objects.filter(id__lt=self.id, status=0).first()




    class Meta:
        ordering = ['-create_time']
        get_latest_by = 'create_time'
        verbose_name = u'文章'
        app_label = 'blog'




class OnlineArticle(models.Model):

    title = models.CharField(max_length=255,unique=True,verbose_name=u'标题')
    content = models.TextField(verbose_name=u'正文')
    author_info = models.CharField(max_length=255, verbose_name=u'作者信息')
    category = models.CharField(max_length=255,verbose_name=u'类别')
    url = models.CharField(max_length=255, default='http://dailyblog.applinzi.com', verbose_name=u'链接')
    finish = models.IntegerField(default=0,verbose_name=u'转载状态')
    create_time = models.DateTimeField(auto_now_add=True)


    def __unicode__(self):
         return '%s' % self.title

    @classmethod
    @mycache.cached(300)
    def get_latest_articles(cls,category=None):
        if category is None:
            return cls.objects.filter(finish=0) \
                   .order_by('-create_time')
        else:
            if category == '经典语录':
                num = 200
                return cls.objects.filter(finish=0,category=category) \
                   .values('id','title','content','author_info','category','url','create_time') \
                   .order_by('-create_time')[:num]
            else:
                return cls.objects.filter(finish=0,category=category) \
                       .values('id','title','content','author_info','category','url','create_time') \
                       .order_by('-create_time')

    class Meta:
        ordering = ['-create_time']
        verbose_name = '在线好文'
        app_label = 'blog'





