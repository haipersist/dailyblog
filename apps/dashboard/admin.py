# -*- coding: utf-8 -*-



from django.contrib import admin
from models import VisitIp,VisitPv


# Register your models here.

#@admin.register(VisitIp)
class VisitIpAdmin(admin.ModelAdmin):
    list_filter = ['ip','visit_day']
    list_display = ['ip','visit_day']
    search_fields = ['ip','visit_day']


#@admin.register(VisitPv)
class VisitPvAdmin(admin.ModelAdmin):
    list_filter = ['page','visit_day']
    list_display = ['page','visit_day']
    search_fields = ['page','visit_day']







