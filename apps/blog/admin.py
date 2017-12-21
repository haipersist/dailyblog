# -*- coding: utf-8 -*-



from django.contrib import admin
from models import Category,Article


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_filter = ['name','alias','status']
    list_display = ['name','alias','status','create_time']
    search_fields = ['name','alias']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_filter = ['category','status']
    list_display = ['title','tags','category','author','pub_time']
    ordering = ['-pub_time',]
    search_fields = ['name','alias']









