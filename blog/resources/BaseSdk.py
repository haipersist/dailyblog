#!/usr/bin/env python
#encoding:utf8


"""
base baidu api sdk
Copyright (C): Haibo wang.2016

"""


import random
import json
import urllib2



class BaiduSDK():

    def __init__(self,url):
        self.base_url = 'http://apis.baidu.com'
        self.apikey = "603fcd2d6312152d404e9d7f893f663e"
        self.url = '/'.join([self.base_url,url])

    def get_content(self):
        request = urllib2.Request(self.url)
        request.add_header("apikey", self.apikey)
        response = urllib2.urlopen(request)
        content = response.read()
        if content:
            return json.loads(content)
        else:
            return None


if __name__ == '__main__':
    keywords = ['生活','坚持','宽容','爱','信任','人生']
    page,rows,keyword = random.choice(range(3)),random.choice(range(20)),random.choice(keywords)
    url = 'avatardata/mingrenmingyan/lookup?dtype=JSON&keyword=%s&page=%d&rows=%d' %(keyword,page,rows)
    logion = BaiduSDK(url)
    result = logion.get_content()['result']
    try:
        index = random.choice(range(len(result)))
        result = result[index]
    except:
        print len(result)
    print '--'.join([result['famous_saying'],result['famous_name']])

