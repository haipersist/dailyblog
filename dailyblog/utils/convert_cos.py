# -*- coding:utf-8 -*-


from __future__ import unicode_literals

from blog.models import Article
from bs4 import BeautifulSoup
from utils.cos_client import Client



def convert():
    articles = Article.objects.all()
    for article in articles:
        content = article.content_html
        content = BeautifulSoup(content,'html5lib')
        imgs = content.find_all("img")
        client = Client()
        if imgs:
            for item in imgs:
                src = item['src']
                if 'sinaapp' not in src:
                    continue
                picture = src.split('/')[-1]
                picture = client.baseurl + picture
                item['src'] = picture
        content = content.body.prettify().replace('<body>', '')
        content = content.replace('</body>', '')
        article.content = content
        article.ck_save()






