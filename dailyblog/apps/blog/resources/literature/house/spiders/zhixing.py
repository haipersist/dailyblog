 # -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider,Rule
from blog.resources.literature.house.items import HouseItem
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import requests
from cStringIO import StringIO
from urlconf import JiSanwen,JiJinpin
from scrapy.http import Request,FormRequest
from blog.resources.baseclass.base_spider import Base_Spider


class ZxSpider(CrawlSpider):
    name = 'zhixing'

    def start_requests(self):
        spider = Base_Spider('zhixing',['Host','Origin','Referer'])
        posturl = 'http://zhixing.bjtu.edu.cn/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'
        postdata = {
            'username':'hbnn',
            'password':'3df693316de6b0511d314b4487b8ad25',
            'quickforward':'yes',
            'handlekey':'ls'
        }
        cookies = spider.login(posturl,postdata)
        """
        cookies = {
            'zhixing_9328_lip': '202.106.86.136%2C1484811340',
            'zhixing_9328_ulastactivity': '9831exMctgUv9w3oAJOJqwPiG%2F02nPgS3OWbektg0FuE8TUHv2xT',
            'zhixing_9328_saltkey': 'ttXqk9T1',
            'zhixing_9328_lastvisit': '1484808041',
            'BIGipServerzhixing_80_v4': '1822060746.20480.0000',
            'zhixing_9328_lastact': '1484811641%09member.php%09logging',
            'zhixing_9328_auth': 'e6621XUvQbqMrxi28YwSTsg%2BvWmNWiJ1gQsioRb%2FTiDetwo0WzO5xQzLOfEPURuPVEp33js2qTbnGSjOjSMxptkZ0g',
            'zhixing_9328_sid': 'qlIiMx',
            'zhixing_9328_checkfollow': '1',
            'zhixing_9328_lastcheckfeed': '11322%7C1484811641'
        }
        """
        url = 'http://zhixing.bjtu.edu.cn/thread-1047622-1-1.html'
        headers = {
            'Host':'zhixing.bjtu.edu.cn',
            'Origin':'http://zhixing.bjtu.edu.cn',
            'Referer':'http://zhixing.bjtu.edu.cn/portal.php',
            'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6'
        }
        return [Request(url,cookies=cookies,callback=self.parse_page,headers=headers)]

    def parse_page(self,response):
        sel = Selector(response)
        r = sel.xpath('//td[@id="postmessage_10415551"]/text()').extract_first()
        print r
        return r










