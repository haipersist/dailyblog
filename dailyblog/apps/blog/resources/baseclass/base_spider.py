#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import requests
import json
import re
import os
import ConfigParser 
from bs4 import BeautifulSoup
from cStringIO import StringIO
import cookielib
import xml.etree.ElementTree as ET
from utils.get_user_agent import get_user_agent
from config import ByrCfg,Job51Cfg,ZhiCfg,LgCfg,DjCfg,WechatCfg,ZhixingCfg

class Base_Spider(object):

    def __init__(self,sitename,*args):
        """
        it's the name of the website that you'll visit,
        it's used to get config info from config file
        """
        self.sitename = sitename
        self.setHeaders(*args)


    def setHeaders(self,*args):
        '''
        add header in order to model explorer,including:
        User-Agent,Referer,Host
        :return:None
        '''
        self.headers = {}
        self.headers.setdefault('User-Agent',get_user_agent())
        for key in args[0]:
            self.get_cfg(self.headers,key)


    def get_cfg(self,field,key):
        SiteCfg = {'byr':ByrCfg(),
                   'lagou':LgCfg(),
                   'zhilian':ZhiCfg(),
                   '51job':Job51Cfg(),
                   'dajie':DjCfg(),
                   'zhixing':ZhixingCfg(),
                   'wechat':WechatCfg()}
        self.cfg = SiteCfg[self.sitename]
        if key == 'X-Requested-With':
            field[key] = getattr(self.cfg,'X_Requested_With')
        else:
            field[key] = getattr(self.cfg,key)


    def build_opener(self,save = False):
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
        #download cookie in order to post data for logining
        #h = urllib2.urlopen(self.host_url)


    def login(self,posturl,postdata):
        '''
        self.build_opener()
        postdata = urllib.urlencode(postdata)
        request = urllib2.Request(url=posturl,data=postdata,headers=self.headers)
        #print self.opener.open(request)
        resp = urllib2.urlopen(request).read()
        print resp
        '''
        self.session = requests.Session()
        r = self.session.post(posturl,data=postdata,headers=self.headers)
        return dict(r.cookies) if not isinstance(r.cookies,dict) else r.cookies


    # get content which is in three different data format
    def get_content(self,url,url_type='html',cookies=None):
        if 'X-Requested-With' not in self.headers.keys():
            #content = urllib2.urlopen(url)
            if cookies is None:
                content = requests.get(url,headers=self.headers)
            else:
                content = requests.get(url,headers=self.headers,cookies=cookies)
            try:
                #get original data brfore transferring unicode
                content = content.content
            except UnicodeEncodeError:
                content = content.text.encode('utf-8')
            except UnicodeDecodeError:
                print 'test'
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
        content = StringIO(content)
        #print content.read(),'test cstr'
        if url_type == 'json':
            return json.load(content)
        elif url_type == 'xml':
            return ET.parse(content)
        else:
            return BeautifulSoup(content,"html5lib")

    def login_get_content(self,url,url_type='html'):
        content = self.session.get(url,timeout = 15)
        try:
            #get original data brfore transferring unicode
            content = content.content
        except UnicodeEncodeError:
            content = content.text.encode('utf-8')
        except UnicodeDecodeError:
            print 'test'
            content = content.text
        content = StringIO(content)
        #print content.read(),'test cstr'
        if url_type == 'json':
            return json.load(content)
        elif url_type == 'xml':
            return ET.parse(content)
        else:
            return BeautifulSoup(content,"html5lib")

    def store(self):
        pass

    def upload_file(self,url,filename):
        with file(filename,'rb') as f:
            requests.post(url,data=f)

    def download(self,imgurl,filename):
        resp = requests.get(imgurl)
        with file(filename,'wb') as f:
            f.write(resp.content)


if __name__ == "__main__":
    spider = Base_Spider('zhixing',['Host','Origin','Referer'])
    print spider.headers
    posturl = 'http://zhixing.bjtu.edu.cn/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'
    postdata = {
        'username':'hbnn',
        'password':'3df693316de6b0511d314b4487b8ad25',
        'quickforward':'yes',
        'handlekey':'ls'
    }
    cookies = spider.login(posturl,postdata)
    print cookies
    url = 'http://zhixing.bjtu.edu.cn/thread-1047622-1-1.html'
    r = spider.login_get_content(url)
    #r = spider.get_content(url,cookies=cookies)
    print r.find(id="thread_subject").string


