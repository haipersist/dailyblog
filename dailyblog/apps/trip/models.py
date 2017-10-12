# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from django.db import models
import random
from datetime import  date
from django.conf import settings
# Create your models here.



#this should be setted in settings.
DEFAULT_IMG  = settings.STATIC_CLOUD_STORE + 'defaultimg.jpg'




FIGURE = {
    'effect-lily':'lily',
    'effect-layla':'layla',
    'effect-roxy':'roxy',
    'effect-sarah':'sarah',
    'effect-milo':'milo',
    'effect-sadie':'sadie',
    'effect-bubba':'bubba',
    'effect-romeo':'romeo',
    'effect-honey':'honey',
    'effect-oscar':'oscar',
    'effect-marley':'marley',
    'effect-chico':'chico',
    'effect-zoe':'zoe',
}





class Trip(models.Model):
    title = models.CharField(max_length=255)
    img = models.CharField(max_length=255,default=DEFAULT_IMG)
    abstract = models.CharField(max_length=255)
    article_url = models.CharField(max_length=100)
    figure_type = models.CharField(default=random.choice(FIGURE.keys()),
                                   max_length=20,
                                   choices=FIGURE.items())
    trip_date = models.DateField()

    def __unicode__(self):
        return "{0} date:{1}".format(self.title,self.trip_date)

    class Meta:
        ordering = ['-trip_date']
        get_latest_by = 'trip_date'
        verbose_name = '旅游记录'
        app_label = 'trip'


    @classmethod
    def latest(cls,field_name=None):
        if field_name is None:
            if not hasattr(cls.Meta,'get_latest_by'):
                return None
        return cls.objects.latest(field_name=field_name)


    @classmethod
    def trip_by_year(cls,year=None):
        if year is None:
            year = date.today().year
        return cls.objects.filter(trip_date_year=year)
