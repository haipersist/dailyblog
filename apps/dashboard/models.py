# -*- coding: utf-8 -*-



from __future__ import unicode_literals

from django.db import models
from datetime import date,datetime,timedelta
# Create your models here.
from utils.cache import Cache



cache = Cache()



class VisitIp(models.Model):

    ip = models.CharField(max_length=64,verbose_name='Ip')
    visit_times = models.IntegerField(blank=True,verbose_name='visit_times_of_one_ip')
    visit_day = models.DateField()

    def __unicode__(self):
         return '%s' % self.ip

    class Meta:
        ordering = ['-visit_day']
        verbose_name = 'VisitIp'
        app_label = 'dashboard'

    @classmethod
    def daily_stat(cls,day=date.today()):
        total_ip = cls.objects.filter(visit_day=day).aggregate(total_ip=models.Count('ip'))
        single_ip_number = cls.objects.filter(visit_day=day).values('ip').annotate(models.Count('ip'))
        return total_ip,single_ip_number

    @classmethod
    def serid_stat(cls,start_date,end_date):
        if end_date is None:
            end_date = date.today()
        else:
            if not isinstance(end_date,date):
                end_date = end_date.strptime("%Y-%m-%d")

        if start_date is None:
            start_date = end_date - timedelta(days=7)
        else:
            if not isinstance(start_date,date):
                start_date = start_date.strptime("%Y-%m-%d")

        if start_date > end_date:
            start_date, end_date = end_date, start_date

        serid_ip = cls.objects.filter(visit_time__range=(start_date,end_date))\
            .values('visit_day').annotate(num_ips=models.Q('ip'))

        return serid_ip


class VisitUv(models.Model):

    uv = models.IntegerField(verbose_name='uv_numbers')
    visit_day = models.DateField()

    def __unicode__(self):
        return "{0}:{1}".format(self.visit_day,self.uv)



class VisitPv(models.Model):

    pv = models.IntegerField(verbose_name='pv_numbers')
    visit_day = models.DateField()

    def __unicode__(self):
        return "{0}:{1}".format(self.visit_day,self.pv)
