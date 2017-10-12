#!/usr/bin/env python
#encoding:utf8

import random
from .BaseSdk import BaiduSDK

def get_logion():
    """
    keywords = ['生活','坚持','宽容','爱','信任','人生','信任','家人']
    page,rows,keyword = random.choice(range(3)),random.choice(range(10)),random.choice(keywords)
    url = 'avatardata/mingrenmingyan/lookup?dtype=JSON&keyword=%s&page=%d&rows=%d' %(keyword,page,rows)
    logion = BaiduSDK()
    result = logion.get_json_content(url)['result']
    index = random.choice(range(len(result)))
    result = result[index]
    famous = '--'.join([result['famous_saying'],result['famous_name']])
    """
    return u'顺，不妄喜；逆，不惶馁；安，不奢逸；危，不惊惧；胸有惊雷而面如平湖者，可拜上将军。'




