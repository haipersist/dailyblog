#!/usr/bin/env python
#encoding:utf8


"""
base baidu api sdk
Copyright (C): Haibo wang.2016

"""


import random
import sys
import json
import urllib2



class BaiduSDK():

    def __init__(self):
        self.base_url = 'http://apis.baidu.com'
        self.apikey = "603fcd2d6312152d404e9d7f893f663e"

    def _get_resp(self,url):
        self.url = '/'.join([self.base_url,url])
        request = urllib2.Request(self.url)
        request.add_header("apikey", self.apikey)
        response = urllib2.urlopen(request)
        return response.read()

    def get_json_content(self,url):
        content = self._get_resp(url)
        if content:
            print content
            return json.loads(content)
        else:
            return None





if __name__ == '__main__':
    ip = '202.106.86.136'
    url = '/txapi/dictum/dictum'
    ipinfo = BaiduSDK()
    resp = ipinfo.get_json_content(url)
    print resp['newslist'][0]['content']



