#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib2
from blog.resources.baseclass.base_spider import Base_Spider
import requests
from papercode import PaperCode

class ParseError(Exception):
    def __init__(self,msg):
        self.msg =msg

    def __str__(self):
        return self.msg



class Wechat_Spider(Base_Spider):

    def __init__(self,website,*args):
        super(Wechat_Spider,self).__init__(website,args)

    def test_parse(self,url):
        soup = None
        try:
            soup = self.get_content(url)
        except urllib2.URLError:
            try:
                soup = self.get_content(url)
            except urllib2.URLError:
                soup = self.get_content(url)
        return soup

    def parse(self,url):
        soup = None
        try:
            soup = self.get_content(url)
        except urllib2.URLError:
                soup = self.get_content(url)

        if not soup:
            #raise ParseError(u'不能正确爬取原文内容，请检查爬虫')
            soup = self.get_content(url)

        title = soup.find(id='activity-name').text
        postuser = soup.find(id='post-user').text
        content_html = soup.find(id='js_content')
        pc = PaperCode()
        for img in content_html.find_all('img'):
            url = img['data-src']
            if url:
                #print url
                stor_name = url.split('/')[4]
                img['data-src'] = pc.store_weixin_pic(url,stor_name)
                img['data-w'] = "90%"
                if img.get('style') is not None:
                    del img['style']
                if img.get('width') is not None:
                    del img['width']
            else:
                pass
        #print content_html
        orig_content = []
        for p in content_html.children:
            if p is None or p.name is None:
                pass
            else:
                if p.string is not None:
                    orig_content.append(p.string)
                    if len(orig_content)>200:
                        break
        abstract =  unicode(','.join(orig_content)[1:300])
        abstract = abstract if abstract else title
        content_html = unicode(content_html).replace('data-src','src')
        content_html = content_html.replace('data-w','width')
        article = {'title':unicode(title),
                   'content':content_html,
                   'abstract':abstract,
                   'postuser':unicode(postuser),
                   'tags':u'微信转载'}

        return article




if __name__ == "__main__":
    wespider = Wechat_Spider('wechat','Host')
    #url = 'http://mp.weixin.qq.com/s?__biz=MzAxMjMzMDYyNg==&mid=2650375414&idx=3&sn=1f5a4a6c27c67fb52ec3202c73cfee49&chksm=83be571bb4c9de0d53344cab0eb8645de3cce807c3a147b57e298d0d94925c224cdb113fb8e4&scene=0#rd'
    #url = 'http://mp.weixin.qq.com/s?__biz=MzA5NzI3MzkxOA==&mid=2653149375&idx=2&sn=4aa8c0a46a16f6b9f57ca73b8c0bec1c&chksm=8b7429eebc03a0f85efca7ff0d0191293cd10f5a2e1b9e23e49454fe708a608e8989327740a3&scene=0#rd'
    url = 'http://mp.weixin.qq.com/s?__biz=MzA4MjEyNTA5Mw==&mid=2652564716&idx=2&sn=ef114d3b5c759d796c93a82fc3e08191&chksm=8464c4a6b3134db0d4eeb8059a6289fe1d3210b5f1dc91bcf6a0f5028bd5d982be015db3405e&scene=0#rd'
    article = wespider.parse(url)
    print article
    #url = 'http://mmbiz.qpic.cn/mmbiz_jpg/xT7HhqxbiboHpZnmaTH3USVkCUVBqE8WhctenvGuFAcj1va0qWiaibNmwctTuWMT2mRWW1Ribs6yfh6icjEhbbLbDsQ/0?wx_fmt=jpeg'
    #print url.split('/')[4]




