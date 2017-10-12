# -*- coding: utf-8 -*-

"""
Account Models are used to create,modify ,delete and query user for blog.
the Base User model is the internal model from django:User.

I define one model called Userprofile,which provides some extra information

of website's users.

09 12 2017

"""

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


GENDER = {
    '男':'boy',
    '女':'girl'
}



# Create your models here.
class UserProfile(models.Model):
    avator = models.ImageField(upload_to='userimg',blank=True)
    age = models.IntegerField(null=True,blank=True,default=0)
    school = models.CharField(max_length=48,blank=True)
    gender = models.CharField(default='男',max_length=10,choices=GENDER.items())
    hobby = models.CharField(max_length=255,blank=True)
    user = models.OneToOneField(User,unique=True)
    motto = models.CharField(max_length=255,blank=True)
    self_introduction = models.TextField(blank=True)
    #phone = models.Ch arField(max_length=13,blank=True)
    birthday = models.DateField(null=True,blank=True,default='2000-01-01')

    def __unicode__(self):
        """
        __str__会调用__unicode__
        :return:
        """
        return "{0} profile".format(self.user.username)

    class Meta:
        db_table = 'user_profile'

    @classmethod
    def exist_user_profile(cls,user):
        if not isinstance(user,models.Model):
            raise TypeError('the user must be one model:User')
        if not cls.objects.filter(user=user):
            return False
        return True





