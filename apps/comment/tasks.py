#from __future__ import unicode_literals
#-*- coding:utf-8 -*-


import os
from ..blog.models import Article
from dailyblog import celery_app
import logging
from django.core.mail import send_mail



logger = logging.getLogger(__name__)

@celery_app.task
def inform_commenter(article_alias,receiver='393993705@qq.com'):
    article_url = Article.get_url_with_domain(article_alias)
    message = "\n".join([
        u'您在千与千寻网站上的评论有回复啦，快点击查看吧:',
        article_url,
    ])
    try:
        send_mail(u'千与千寻网站有给您的回复啦', message, None, [receiver])
    finally:
        return 'new comment'




