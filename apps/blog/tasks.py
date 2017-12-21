#from __future__ import unicode_literals
#-*- coding:utf-8 -*-


import os
from django.db.models import F
from models import Article
from dailyblog import celery_app
from utils.cos_client import Client
from utils.imgcompress import ImageThumb
from bs4 import BeautifulSoup
from django.conf import settings
import logging
from ..trip.models import Trip
from django.core.mail import send_mail
from weiborobot import WeiboRobot
from django.conf import settings



logger = logging.getLogger(__name__)

@celery_app.task
def incr_readtimes(article_id):
    return Article.objects.filter(id=article_id).update(read_times=F('read_times') + 1)


@celery_app.task
def add_trip(article_url,title,img,abstract,trip_date):
    trip = Trip(
        title=title,
        article_url=article_url,
        abstract=abstract,
        img=img,
        trip_date=trip_date
    )
    trip.save()
    return 'success'

@celery_app.task
def inform_commenter(article_alias,receiver='393993705@qq.com'):
    article_url = Article.get_url_with_domain(article_alias)
    message = "\n".join([
        u'您在千与千寻网站上的评论有回复啦，快点击查看吧:',
        article_url,
    ])
    try:
        send_mail('千与千寻网站有给您的回复啦', message, None, [receiver])
    finally:
        return 'new comment'



#@celery_app.task
def change_img(alias):
    article = Article.objects.get(alias=alias)
    content = article.content
    content = BeautifulSoup(content, "html5lib")
    imgs = content.find_all("img")
    client = Client()
    img_thumb = ImageThumb()
    if not imgs:
        return article.content
    for item in imgs:
        src = item['src']
        if 'blog' in src:
            continue
        if 'static' in src:
            continue
        filepath = '/srv/dailyblog/www' + src
        logger.info(filepath)
        #try:
        upfile = img_thumb.thumbnail(filepath)
        online_url = client.upload(upfile)
        #the file uploading maybe uploaded before
        if isinstance(online_url,dict):
            p,f = os.path.split(filepath)
            if online_url['fail'] == u'ERROR_CMD_COS_FILE_EXIST':
                online_url = client.baseurl + f
            else:
                continue
        item['src'] = online_url
        logger.info(online_url)
        os.remove(filepath)
        p, pic_format = os.path.splitext(filepath)
        thumb_format = p + '_thumb' + pic_format
        if os.path.exists(thumb_format):
            os.remove(thumb_format)
        #except:
        #    continue

    content = content.body.prettify().replace('<body>', '')
    content = content.replace('</body>', '')
    article.content = content
    article.ck_save()
    return content





@celery_app.task
def repost_weibo(article_title,article_alias):
    weconfig = settings.WEIBO
    weibo = WeiboRobot(
            weconfig['USERNAME'],
            weconfig['PASSWORD'],
            weconfig['APP_KEY'],
            weconfig['APP_SECRET']
            )
    text = u'程序分享文章：' +article_title + settings.DOMAIN + 'article/' + article_alias + '.html'
    weibo.communicate('/statuses/share','post',status=text)
    return 'send weibo about created article'








