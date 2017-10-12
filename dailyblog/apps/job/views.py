# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic import ListView,DetailView
from models import Job
from datetime import date
from django.conf import settings
from ..blog.views import BaseMixin
# Create your views here.

class JobView(BaseMixin,ListView):
    template_name = 'job/job.html'
    context_object_name = 'job_list'
    queryset = Job.objects.filter(pub_time__year=date.today().year)
    paginate_by = settings.NUM_PER_PAGE

    def get_context_data(self,*args,**kwargs):
        context = super(JobView,self).get_context_data(**kwargs)
        context['title'] = u'千与千寻'
        return context


