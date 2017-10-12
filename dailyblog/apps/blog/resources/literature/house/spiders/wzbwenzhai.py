 # -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider,Rule
from blog.resources.literature.house.items import HouseItem
from scrapy.selector import Selector
#from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import requests
from cStringIO import StringIO
import scrapy
from urlconf import WzbWenzhai



class WzbWzspider(CrawlSpider):
    name = 'wzbwz'

    def start_requests(self):
        url = WzbWenzhai().request_url
        yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):
        content = response.body
        if not content:
            self.log('the content is empty')
            return
        sel = Selector(response)
        item = HouseItem()
        for source in sel.xpath('//ul[@class="index_list_source"]/li'):
            #/ means root directory,// means any directory
            item['title'] = source.xpath('a/text()').extract_first()
            item['url'] = WzbWenzhai().base_url + source.xpath('a/@href').extract_first()
            item['author_info'] = u'文摘'
            item['category'] = u'文摘大全'
            yield item






