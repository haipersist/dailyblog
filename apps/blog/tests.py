#!/usr/bin/env python
#encoding:utf-8

from django.test import TestCase
from blog.models import Article,Category
from django.contrib.auth.models import User

# Create your tests here.


class CategoryTestCase(TestCase):
    def setUp(self):
        Category.objects.create(name='testcat',alias='cat')

    def test_cat_status(self):
        cat = Category.objects.get(name='testcat')
        self.assertEqual(cat.status,0)



class ArticleTestCase(TestCase):
    def setUp(self):
        cat = Category.objects.create(name='testarticle',alias='article')
        user = User.objects.create(username='haibo',password='haibo',email='3934354@qq.com')
        Article.objects.create(name='test',alias='test',content='test',tags='test',author=user,category=cat)
        Article.objects.create(name='test',alias='test',content='test',tags='test',author=user,category=cat,access=200)

    def test_article_base_attr(self):
        article = Article.objects.get(name='test')
        article2 = Article.objects.get(name='test')
        self.assertEqual(article.status,0)
        self.assertEqual(article.read_times,0)
        self.assertEqual(article.access,100)
        self.assertEqual(article2.access,200)

    def test_article_tag_list(self):
        article = Article.objects.get(name='test')
        self.assertEqual(article.tag_list,['test'])







