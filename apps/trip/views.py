#-*- coding:utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render
from ..blog.views import BaseMixin
from django.views.generic import ListView
from models import Trip



# Create your views here.

class TripIndexView(BaseMixin,ListView):
    template_name = 'trip/tripindex.html'
    #paginate_by = NUM_PER_PAGE
    context_object_name = 'trip_list'

    def get_queryset(self):
        self.trip_list = Trip.objects.all()
        return self.trip_list

    def get_context_data(self,*args,**kwargs):
        context = super(TripIndexView,self).get_context_data(**kwargs)
        context['trip_module'] = u'欢迎欣赏我的旅游日记'
        return context

