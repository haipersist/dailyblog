# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import requests
import datetime

class JsonWriterPipeline(object):

    def __init__(self):
        self.day = datetime.date.today().strftime("%Y-%m-%d")
        self.file = codecs.open('store_%s.html'%self.day,'w',encoding='utf8')
        
    def process_item(self, item, spider):
        result = {}
        for key in item:
            result[key] = item[key]
        line = json.dumps(result,ensure_ascii=False) + "\n"
        self.file.write(line)
        r = requests.post('http://dailyblog.applinzi.com/api/onlines/',data=result, auth=('haibo_persist','NANAnana320'))
        return item

    def close_spider(self,spider):
        #when the spider is closed ,the method will be called
        self.file.close()




