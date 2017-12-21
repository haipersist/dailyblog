# -*- coding: utf-8 -*-

import urllib2
import json
from cStringIO import StringIO
import cookielib
import xml.etree.ElementTree as ET
import random
import requests
from bs4 import BeautifulSoup

#from webspider.config.websetting import USER_AGENTS,ZLCfg


class Base_Spider(object):

    def __init__(self,obj):
        """
        it's the name of the website that you'll visit,
        it's used to get config info from config file
        obj is one class of ByrCfg,LgCfg etc.
        """
        self.obj = obj
        self.session = requests.Session()
        self._setHeaders()


    def _setHeaders(self):
        USER_AGENTS = [
            'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31',

            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17',

        ]
        '''
        add header in order to model explorer,including:
        User-Agent,Referer,Host
        :return:None
        '''
        self.headers = {}
        self.headers.setdefault('User-Agent',random.choice(USER_AGENTS))
        if hasattr(self.obj,'header'):
            self.headers.update(self.obj.header())

    def login(self,posturl,postdata):
        """
        the class use requests module,session instance
        it will return the cookie after successful login

        :param posturl:the real url that used to post login data
        :param postdata:the form data ,that is your accunt
        :return:
        """
        r = self.session.post(posturl,data=postdata)
        return dict(r.cookies) if not isinstance(r.cookies,dict) else r.cookies


    def get_content(self,url,url_type='html', method='GET',data=None):
        """
         get content which is in three different data format
        :param url:
        :param url_type:
        :param cookies:
        :return:
        if 'X-Requested-With' not in self.headers.keys():
            #content = urllib2.urlopen(url)
            content = requests.get(url,headers=self.headers)
            try:
                #get original data brfore transferring unicode
                content = content.content
            except UnicodeEncodeError:
                content = content.text.encode('utf-8')
            except UnicodeDecodeError:
                content = content.text
        else:
            opener = self.build_opener()
            header_list = []
            for key in self.headers.keys():
                header_list.append((key,self.headers[key]))
            opener.addheaders = header_list
            content = opener.open(url).read()
            try:
                if not isinstance(content,basestring and unicode):
                        content = content.decode('GBK').encode('utf8')
            except UnicodeDecodeError:
                pass
        """
        if method == 'GET':
            content = self.session.get(url,timeout = 15,headers=self.headers)
        if method == 'POST':
            content = self.session.post(url,
                                        timeout=15,
                                        headers=self.headers,
                                        data=data
                                        )
        #print dict(content.cookies),'cookies'
        try:
            #get original data brfore transferring unicode
            content = content.content
        except UnicodeEncodeError:
            content = content.text.encode('utf-8')
        except UnicodeDecodeError:
            content = content.text
        #if not isinstance(content,basestring and unicode):
        #   content = content.decode('GBK').encode('utf8')
        content = StringIO(content)
        if url_type == 'json':
            return json.load(content)
        elif url_type == 'xml':
            return ET.parse(content)
        else:
            return BeautifulSoup(content,"html5lib")

    def upload_file(self,url,filename):
        with file(filename,'rb') as f:
            requests.post(url,data=f)

    def download(self,imgurl,filename):
        resp = requests.get(imgurl)
        with file(filename,'wb') as f:
            f.write(resp.content)

    def build_opener(self,save = False):
        """
        this method is also used to login ,but I don't often use it.
        :param save:
        :return:
        """
        if not save:
            cj = cookielib.LWPCookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj),
                                          urllib2.HTTPHandler)
        else:
            cj =cookielib.MozillaCookieJar()
            cj.save('cookie.txt',ignore_discard=True,ignore_expires=True)
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        return opener


