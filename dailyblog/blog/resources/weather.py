#!/usr/bin/env python
#encoding:utf8


import datetime
from .BaseSdk import BaiduSDK


def get_weathe_info():
    url = 'apistore/weatherservice/weather?citypinyin=beijing'
    weather = BaiduSDK(url)
    result = weather.get_content()['retData']
    weather_info = ' '.join([
        u'今天是%s' % datetime.date.today().strftime('%Y-%m-%d'),
        u'%s' % result['city'],
        u'%s' % result['weather'],
        u'温度：%s℃' % result['temp'],
        u'风力：%s' % result['WS'],
        u'风向：%s' % result['WD'],
        u'最低气温：%s℃' % result['l_tmp'],
        u'最高气温：%s℃' % result['h_tmp'],
        u'日出时间：%s' % result['sunrise'],
        u'日落时间：%s' % result['sunset'],

    ])
    return weather_info




