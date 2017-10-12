# -*- coding: utf-8 -*-
__author__ = 'WHB'
import urllib2
#import requests
import xml.etree.ElementTree as ET
from cStringIO import StringIO


class Music():

    def __init__(self,content):
        self.title,self.artist = content.split(' ')[0],content.split(' ')[1]
        self.baseurl = u'http://box.zhangmen.baidu.com/x?op=12&count=1&title=%s$$%s$$$$'%\
                       (self.title,self.artist)

    def get_url(self):
        """
        :return:musicurl,hqurl in dict type
        """
        resp = requests.get(self.baseurl).content
        resp = resp.decode('gb2312').encode('utf-8')
        resp = resp.replace('gb2312', 'utf-8')
        root = ET.parse(StringIO(resp))
        url = root.find('url')
        for child in url:
            if child.tag == 'encode':
                url1 = child.text
            if child.tag == 'decode':
                url2 = child.text
        musicurl = '/'.join([url1,url2])
        hqurl = root.find('durl')
        for child in hqurl:
            if child.tag == 'encode':
                hqurl1 = child.text
            if child.tag == 'decode':
                hqurl2 = child.text
        hqurl = '/'.join([hqurl1,hqurl2])
        return {'musicurl':musicurl,'hqurl':hqurl}

MusicDict = {'1':{'title':u'石进-忆','desc':u'爱你',
              'url':'http://hbnnlove-hbnnlove.stor.sinaapp.com/%E7%9F%B3%E8%BF%9B-%E5%BF%86.mp3'},
         '2':{'title':'Marry me','desc':u'爱你,老婆',
              'url':'http://hbnnlove-hbnnlove.stor.sinaapp.com/Train-Marry%20Me.mp3'},
         '3':{'title':u'羽泉-烛光里的妈妈','desc':u'永远在一起',
              'url':'http://hbnnlove-hbnnlove.stor.sinaapp.com/%E7%BE%BD%E6%B3%89-%E7%83%9B%E5%85%89%E9%87%8C%E7%9A%84%E5%A6%88%E5%A6%88.mp3'
         }}



if __name__ == "__main__":
   s = Music(u'逆战 张杰').get_url()
   print s['musicurl']
   print s['hqurl']
