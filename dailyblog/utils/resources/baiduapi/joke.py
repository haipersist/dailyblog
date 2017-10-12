#!/usr/bin/env python
#-*-coding:utf-8-*-


"""
create joke by using baidu api.
must has own app_key in baidu.

Copyright (C): Haibo wang.2016

"""

import sys
import json
import urllib2
import random


def get_joke_text():
    total_pages = 1000
    url = create_url(total_pages)
    text = ''
    try:
        text = parse_url(url)
    except KeyError:
        total_pages = 500
        url = create_url(total_pages)
        text = parse_url(url)
    finally:
        return text



def create_url(total_pages):
    page = random.choice(xrange(total_pages))
    return 'http://apis.baidu.com/showapi_open_bus/showapi_joke/joke_text?page=%d' % page


def parse_url(url):
    request = urllib2.Request(url)
    request.add_header("apikey", "603fcd2d6312152d404e9d7f893f663e")
    response = urllib2.urlopen(request)
    content = response.read()
    if content:
        content = json.loads(content)
        result = content['showapi_res_body']['contentlist']
        index = random.choice(range(len(result)))
        return result[index]['text']

