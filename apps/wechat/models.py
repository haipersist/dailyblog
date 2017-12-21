#from __future__ import unicode_literals
#encoding:utf-8

from django.db import models

# Create your models here.


class WeArticle(models.Model):

    title = models.CharField(max_length=150,unique=True,verbose_name=u'标题')
    desc = models.TextField(verbose_name=u'描述')
    url = models.CharField(max_length=512,verbose_name=u'链接')
    create_time = models.DateTimeField(auto_now_add=True)
    finish = models.IntegerField(default=0,verbose_name=u'转载状态')


    def __unicode__(self):
         return '%s' % self.title

    class Meta:
        ordering = ['-create_time']
        verbose_name = u'微信在线文章'
