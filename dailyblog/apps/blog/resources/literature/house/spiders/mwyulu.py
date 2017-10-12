 # -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider,Rule
from blog.resources.literature.house.items import HouseItem
from scrapy.selector import Selector
#from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import requests
from cStringIO import StringIO
import scrapy
from urlconf import MwYulu



class Mwylspider(CrawlSpider):
    name = 'mwyl'

    def start_requests(self):
        sites = [MwYulu(),]
        urls = []
        for site in sites:
            response = requests.get(site.request_url).content
            response = BeautifulSoup(StringIO(response),'html5lib')
            option = list(response.find('select',attrs={'name':'sldd'}).children)[-2]
            pages = option.string
            pages = int(pages)
            for page in range(1,pages+1):
                url = site.request_url + 'list_%d_%d.html' % (site.list,page)
                urls.append(url)

        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):
        content = response.body
        if not content:
            self.log('the content is empty')
            return
        sel = Selector(response)
        urls = sel.xpath('//ul[@class="picAtc pr"]/li/div[@class="info"]/h3/a/@href').extract()
        for url in urls:
            url = MwYulu().base_url + url
            yield scrapy.Request(url=url,callback=self.parse_items)

    def parse_items(self,response):
        """
        This method, as well as any other Request callback,
        must return an iterable of Request and/or dicts or Item objects.
        :param response:
        :return:item
        """
        sel = Selector(response)
        item = HouseItem()
        title = sel.xpath('//div[@class="article"]/h1/text()').extract_first()
        authorInfo = sel.xpath('//div[@class="article"]/div[@class="info"]').extract_first()
        content = sel.xpath('//div[@class="article"]/article').extract_first()
        item['title'] = title
        item['content'] = content
        item['author_info'] = authorInfo
        item['category'] = u'经典语录'
        yield item






