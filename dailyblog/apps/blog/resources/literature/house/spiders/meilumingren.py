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
from urlconf import MlYulu


class MlMrspider(CrawlSpider):
    name = 'mlmr'

    def start_requests(self):
        sites = [MlYulu(),]
        urls = []
        for site in sites:
            response = requests.get(site.request_url).content
            response = BeautifulSoup(StringIO(response),'html5lib')
            options = response.find_all('option',attrs={'class':'pageSelect'})
            pages = options[-1]['value']
            pages = int(pages)
            for page in range(1,pages+1):
                url = site.request_url + 'list_%d.html' % page
                print url
                urls.append(url)

        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):
        content = response.body
        if not content:
            self.log('the content is empty')
            return
        sel = Selector(response)
        urls = sel.xpath('//div[@class="article_list_body"]/ul/li[@class="Article_Title"]/a/@href').extract()
        for url in urls:
            url = MlYulu().base_url + url
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
        title = sel.xpath('//div[@class="Article_title"]/dl/dd[1]/text()').extract_first()
        #authorInfo = sel.xpath('//div[@class="art_viewbox bd"]/div[@class="info"]').extract_first()
        content = sel.xpath('//div[@class="Article_body"]/p').extract()
        if content:
            article_content = ' '.join(content) if len(content) > 1 else content[0]
            item['title'] = title
            item['content'] = article_content
            item['author_info'] = u'转载'
            item['category'] = u'经典语录'
            yield item






