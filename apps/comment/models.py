# -*- coding: utf-8 -*-
"""
In Comment Module,I set three models.

   Author:the user who write comments.
   Comment:the comment for article
   ReplyComment:the reply for the above comment.



"""

from __future__ import unicode_literals
from django.db import models
from utils.cache import Cache
from ..blog.models import Article






mycache = Cache()




class Author(models.Model):
    avator = models.ImageField(default='/static/img/hbnn.ico')
    name = models.CharField(max_length=48,default='guest')
    email = models.EmailField(unique=True)

    def __unicode__(self):
        return "{0} by {1}".format(self.name,self.email)

    class Meta:
        app_label = 'comment'



class BaseComment(models.Model):
    """
    create_time,ip fields are public,so I write one abstract base class.
    Comment and ReplyComment is subclass of it

    """
    create_time = models.DateTimeField(auto_now=True)
    ip = models.GenericIPAddressField(protocol='IPv4')


    def save(self,*args,**kwargs):
        """
        try:
            ip_address_validators('ipv4',self.ip)
        except ValidationError:
            return
        """
        super(BaseComment,self).save(*args,**kwargs)


    class Meta:
        #the class is base class,include common info,do not create table
        abstract = True



class Comment(BaseComment):
    content = models.TextField()
    article = models.ForeignKey(Article,verbose_name='原文名字',related_name='comment_article_name')
    author = models.ForeignKey(Author,related_name='pub_comment_author')

    def __unicode__(self):
        return "{0}:{1}".format(self.author,
                                self.create_time.strftime("%Y-%m-%d %H:%M:%S"))

    class Meta:
        ordering = ['-create_time']
        get_latest_by = 'create_time'
        verbose_name = 'comment'
        app_label = 'comment'
        #unique_together = ('author','content')



class ReplyComment(BaseComment):
    content = models.TextField()
    comment = models.ForeignKey(Comment,related_name='reply_comment')
    author = models.ForeignKey(Author,related_name='reply_comment_author')
    reply_to = models.ForeignKey(Author,related_name='reply_to_author')


    def __unicode__(self):
        return "{0}@{1}".format(self.author,self.reply_to)


    class Meta:
        ordering = ['create_time']
        verbose_name = 'replycomment'
        get_latest_by = 'create_time'
        app_label = 'comment'



