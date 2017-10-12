#!/usr/bin/env python
# -*- coding: utf-8 -*-



import random
from utils.cookie2scrapy import cookie2scrapy


USER_AGENTS = [
            'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31',

            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17',

            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',\
            'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
            'Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',

            'Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1',
            'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1',
            'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:15.0) Gecko/20120910144328 Firefox/15.0.2',

            'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9a3pre) Gecko/20070330',
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.13; ) Gecko/20101203',
            'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
            'Opera/9.80 (X11; Linux x86_64; U; fr) Presto/2.9.168 Version/11.50',
            'Mozilla/5.0 (Windows; U; Win 9x 4.90; SG; rv:1.9.2.4) Gecko/20101104 Netscape/9.1.0285',
            'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.8.1.7pre) Gecko/20070815 Firefox/2.0.0.6 Navigator/9.0b3',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
        ]


def get_user_agent(func):
    def wrapper():
        result = func()
        if isinstance(result,dict):
            result.update({'User-Agent':random.choice(USER_AGENTS)})
        return result
    return wrapper



class ByrCfg(object):

    @classmethod
    def header(cls):
        return {
            'Host':'www.bbs.byr.cn',
            'Referer':'www.bbs.byr.cn',
            'X_Requested_With':'XMLHttpRequest'
        }

    @classmethod
    def account(cls):
        return {'id':'liangting','passwd':'001108'}


class Job51Cfg(object):

    @classmethod
    def header(cls):
        return {
            'Host':'www.search.51job.com',
            'Cookie':'guid=14465584429375700076; slife=compfans%3D1%257C0%257C0%257C0; search=jobarea%7E%60010000%7C%21ord_field%7E%600%7C%21list_type%7E%600%7C%21recentSearch0%7E%602%A1%FB%A1%FA010000%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA01%A1%FB%A1%FA99%A1%FB%A1%FApython%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1452781332%A1%FB%A1%FA0%A1%FB%A1%FA%7C%21recentSearch1%7E%602%A1%FB%A1%FA010000%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA01%A1%FB%A1%FA99%A1%FB%A1%FAAnroid%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1452781220%A1%FB%A1%FA0%A1%FB%A1%FA%7C%21recentSearch2%7E%602%A1%FB%A1%FA010000%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA01%A1%FB%A1%FA99%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1452780011%A1%FB%A1%FA0%A1%FB%A1%FA%7C%21recentSearch3%7E%602%A1%FB%A1%FA010000%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FAAnroid%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1452781294%A1%FB%A1%FA0%A1%FB%A1%FA%7C%21recentSearch4%7E%602%A1%FB%A1%FA010000%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FApython%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1452781317%A1%FB%A1%FA0%A1%FB%A1%FA%7C%21; guide=1; collapse_expansion=1; nolife=fromdomain%3D; ps=us%3DCzFUPVIyBi5RMQ1jBmtWewc1CzlVZVYtBjFUPwg3BXlbYlM8B2BXYwBmWz9XM1ZmV2RWYwQ0BWQANwUrXDAHVAtmVDhSVA%253D%253D; 51job=cenglish%3D0'
        }


    @classmethod
    def cookies(cls):
        return {
            'guid':'14465584429375700076',
            'slife':'compfans%3D1%257C0%257C0%257C0',
            'search':'jobarea%7E%60010000%7C%21ord_field%7E%600%7C%21list_type%7E%600%7C%21recentSearch0%7E%602%A1%FB%A1%FA010000%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA01%A1%FB%A1%FA99%A1%FB%A1%FApython%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1452781332%A1%FB%A1%FA0%A1%FB%A1%FA%7C%21recentSearch1%7E%602%A1%FB%A1%FA010000%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA01%A1%FB%A1%FA99%A1%FB%A1%FAAnroid%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1452781220%A1%FB%A1%FA0%A1%FB%A1%FA%7C%21recentSearch2%7E%602%A1%FB%A1%FA010000%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA01%A1%FB%A1%FA99%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1452780011%A1%FB%A1%FA0%A1%FB%A1%FA%7C%21recentSearch3%7E%602%A1%FB%A1%FA010000%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FAAnroid%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1452781294%A1%FB%A1%FA0%A1%FB%A1%FA%7C%21recentSearch4%7E%602%A1%FB%A1%FA010000%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FApython%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1452781317%A1%FB%A1%FA0%A1%FB%A1%FA%7C%21',
            'guide':'1',
            'collapse_expansion':'1',
            'nolife':'fromdomain%3D',
            'ps':'us%3DCzFUPVIyBi5RMQ1jBmtWewc1CzlVZVYtBjFUPwg3BXlbYlM8B2BXYwBmWz9XM1ZmV2RWYwQ0BWQANwUrXDAHVAtmVDhSVA%253D%253D',
            '51job':'cenglish%3D0'

        }


class ZLCfg(object):

    jobhost = 'jobs.zhaopin.com'

    @classmethod
    def header(cls):
        return {
            'Host':'sou.zhaopin.com',
        }

auth = ('haibo_persist','NANAnana320')



class LgCfg(object):

    Cookie = """user_trace_token=20170327064902-b36275bfffde4c5ca209ca81349f8aaa; _ga=GA1.2.344451825.1490568536; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6
=1499929502; LGUID=20170327064902-68464139-1276-11e7-a304-525400f775ce; JSESSIONID=ABAAABAACDBAAIAB1AB69AE1192C8ACC3001B5E7E98558F
; X_HTTP_TOKEN=c39596d4e2fcb5042b60c89b648d0974; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1499929721
; LGSID=20170713150502-972ac068-6799-11e7-a82b-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND
=https%3A%2F%2Fpassport.lagou.com%2Flogin%2Flogin.html%3Fts%3D1499929500812%26serviceId%3Dlagou%26service
%3Dhttp%25253A%25252F%25252Fwww.lagou.com%25252Fjobs%26action%3Dlogin%26signature%3D29AAF895E0021662F49316D0B4D168A6
; LGRID=20170713150840-192d6e84-679a-11e7-b83e-525400f775ce; _gid=GA1.2.291952946.1499929504; _gat=1
; index_location_city=%E5%8C%97%E4%BA%AC; TG-TRACK-CODE=search_code; SEARCH_ID=94054433704c44139fd05
6f489f15c12
            """

    @classmethod
    def header(cls):
        return {
            'Host':'www.lagou.com',
            'X_Requested_With':'XMLHttpRequest',
            'X - Anit - Forge - Code': '0',
            'X - Anit - Forge - Token': None,
            'Referer':'https://www.lagou.com/jobs/list_Python?px=new&gx=%E5%85%A8%E8%81%8C&city=%E5%8C%97%E4%BA%AC',
            'Cookie':cls.Cookie
        }

    @classmethod
    def job_header(cls):
        return {
            'Host': 'www.lagou.com',
            'Cookie': cls.Cookie,
            'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
        }


    @classmethod
    def cookies(cls):
        return cookie2scrapy(cls.Cookie)



class DjCfg(object):

    @classmethod
    def header(cls):
        return {
            'Host':'so.dajie.com',
            'Referer':'http://so.dajie.com/job/search?keyword=python&f=nav',
            'X_Requested_With':'XMLHttpRequest',
            'Cookie':'SO_COOKIE=0118rYGAq6mYqoQMbSISR/nV4+crW0dVqftsEZTM1cHnN93KRvgKDOgbfWMP3Sw+KrUUUvoQEspFD+6H9APzjOnTpIpYG/BZswUX; DJ_UVID=MTQ1ODQ0NDM5OTgzNzU3MjUz; __login_tips=1; DJ_RF=empty; DJ_EU=http%3A%2F%2Fso.dajie.com%2Fjob%2Fsearch%3Fkeyword%3Dpython%26f%3Dnav'
        }



class ZhixingCfg(object):

    @classmethod
    def header(cls):
        return {
            'Host':'zhixing.bjtu.edu.cn',
            'Origin':'http://zhixing.bjtu.edu.cn',
            'Referer':'http://zhixing.bjtu.edu.cn/portal.php',
        }

    @classmethod
    def account(cls):
        return {
            'username':'hbnn',
            'password':'3df693316de6b0511d314b4487b8ad25',
            'quickforward':'yes',
            'handlekey':'ls'
        }

AUTH = ('haibo_persist', 'NANAnana320')


class SmCfg(object):

    @classmethod
    def header(cls):
        return {
            'Host':'www.newsmth.net',
            'Referer':'http://www.newsmth.net/nForum/',
            'X_Requested_With':'XMLHttpRequest',
        }

    @classmethod
    def cookies(cls):
        return {
            "main[UTMPUSERID]": "guest",
            "main[UTMPKEY]": "14694331",
            "main[UTMPNUM]": "3128",
            "Hm_lvt_9c7f4d9b7c00cb5aba2c637c64a41567":"1491892240",
            "Hm_lpvt_9c7f4d9b7c00cb5aba2c637c64a41567":"1491892293",
            "left-index":'00000100000'
        }

class LpCfg(object):

    @classmethod
    def header(cls):
        return {
            'Host':'www.liepin.com',
            'Referer':'https://www.liepin.com/zhaopin/?pubTime=7'
                      '&ckid=f16c108c7de56cec&fromSearchBtn=2&compkind='
                      '&isAnalysis=&init=-1&searchType=1&flushckid=1&dqs=010'
                      '&industryType=&jobKind=2&sortFlag=15&industries=&'
                      'salary=&compscale=&key=Python&clean_condition='
                      '&headckid=0b5a9690a5cb1d82'
        }