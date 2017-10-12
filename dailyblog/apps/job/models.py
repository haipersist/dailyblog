# -*- coding: utf-8 -*-



from __future__ import unicode_literals

from django.db import models
from datetime import date,datetime,timedelta
# Create your models here.
from utils.cache import Cache



cache = Cache()



class Website(models.Model):

    website = models.CharField(max_length=255,unique=True,verbose_name='网站')
    homepage = models.CharField(max_length=255,verbose_name='主页')

    def __unicode__(self):
        return '网站:%s' % self.website

    class Meta:
        verbose_name = '招聘地址'
        app_label = 'job'





class Company(models.Model):

    name = models.CharField(max_length=255,unique=True,verbose_name='名称')
    address = models.CharField(max_length=255,blank=True,verbose_name=u'地址')
    introduction = models.TextField(blank=True,verbose_name='介绍')
    homepage = models.CharField(max_length=255,blank=True,verbose_name='公司主页')


    def __unicode__(self):
         return '公司：%s' % self.name

    @classmethod
    @cache.cached(300)
    def get_all_companies(cls):
        return cls.objects.all()

    class Meta:
        verbose_name = '公司'
        app_label = 'job'


    @classmethod
    def get_xiaomi(cls):
        query_sql =(models.Q(name__icontains='xiaomi') | models.Q(name__icontains='小米'))
        return cls.objects.filter(query_sql)




class Job(models.Model):

    title = models.CharField(max_length=255,verbose_name='职位名称')
    welfare = models.TextField(blank=True,verbose_name='福利')
    requirement = models.TextField(blank=True,verbose_name='职位要求')
    link = models.CharField(max_length=255,verbose_name='链接')
    company = models.ForeignKey(Company,verbose_name='公司')
    website = models.ForeignKey(Website,verbose_name='招聘网站')
    pub_time = models.DateField(blank=True,default=date.today().strftime("%Y-%m-%d"))
    load_time = models.DateTimeField(auto_now=True)
    salary = models.CharField(max_length=127,blank=True,verbose_name='薪资')

    def __unicode__(self):
         return '%s' % self.title

    @classmethod
    def get_certain_jobs(cls,start=None,end=None):
        if end is None:
            end = date.today().strftime("%Y-%m-%d")
        if start is None:
            start = (datetime.strptime(end,"%Y-%m-%d") - timedelta(days=7)).strftime("%Y-%m-%d")
        if start > end:
            start, end = end, start

        start, end = datetime.strptime(start,"%Y-%m-%d"), datetime.strptime(end,"%Y-%m-%d")
        return cls.objects.filter(pub_time__range=(start,end)).order_by('-id')


    @classmethod
    @cache.cached(300)
    def get_jobs_by_comp(cls,company):
        if isinstance(company,int):
            company = Company.objects.get(pk=company)
        elif isinstance(company,models.Model):
            company = company
        else:
            raise TypeError('the company must be one Company model or one integer.')
        return cls.objects.filter(company__iexact=company)

    @classmethod
    @cache.cached(300)
    def get_jobs_by_site(cls,site):
         if isinstance(site,int):
            site = Website.objects.get(pk=site)
         elif isinstance(site,models.Model):
            site = site
         else:
            raise TypeError('the company must be one Website model or one integer.')
         return cls.objects.filter(company__iexact=site)

    @classmethod
    @cache.cached(300)
    def get_all_jobs(cls):
        return cls.objects.all()

    @classmethod
    @cache.cached(300)
    def get_job_count_by_day(cls,start=None,end=None):
        if end is None:
            end = date.today().strftime("%Y-%m-%d")
        if start is None:
            start = (datetime.strptime(end,"%Y-%m-%d") - timedelta(days=7)).strftime("%Y-%m-%d")
        if start > end:
            start, end = end, start



        return cls.objects.filter(pub_time__range=(start,end)) \
            .values("pub_time").annotate(count=models.Count("pub_time")).order_by('pub_time')


    class Meta:
        verbose_name = '工作职位'
        db_table = 'job_detail'
        app_label = 'job'
