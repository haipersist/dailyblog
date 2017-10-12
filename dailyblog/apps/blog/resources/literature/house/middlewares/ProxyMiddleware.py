__author__ = 'wanghb311'
#-*- coding:utf-8 -*-

import requests
import json

proxies = {'http':'http://114.43.226.77:8998',
           }
def check_proxy(proxies):
    resp = requests.get('http://ip.chinaz.com/getip.aspx',timeout=10,proxies=proxies)
    print resp.content

