#!/usr/bin/env python
#encoding:utf8

import random
from .BaseSdk import BaiduSDK

def get_logion():
    """
    keywords = ['生活','坚持','宽容','爱','信任','人生']
    page,rows,keyword = random.choice(range(3)),random.choice(range(10)),random.choice(keywords)
    url = 'avatardata/mingrenmingyan/lookup?dtype=JSON&keyword=%s&page=%d&rows=%d' %(keyword,page,rows)
    logion = BaiduSDK(url)

    try:
        result = logion.get_content()['result']
        index = random.choice(range(len(result)))
        result = result[index]
        return '--'.join([result['famous_saying'],result['famous_name']])
    except:
    """
    return u'人生的意义并不在于你拥有什么，而在于你得到了或失去了什么。说到底，我们活着是为了一个过程，而不是结果。'

