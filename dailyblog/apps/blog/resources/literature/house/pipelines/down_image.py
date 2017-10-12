__author__ = 'BJHaibo'


import os
import scrapy
# from scrapy.spider import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem


class MyImagePipeline(ImagesPipeline):

    def __init__(self,store_uri,download_func=None):
        # store_uri is automatically set from setting.py :IMAGE_STORE
        self.store_path = store_uri
        super(MyImagePipeline,self).__init__(store_uri,download_func=None)

    def get_media_requests(self, item, info):
        url = item.get('url',None)
        if url is not None:
            yield scrapy.Request(url)

    #when the scrapy.Request finished downloading ,the method will be called
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok,x in results if ok]
        if image_paths:
            image_path = image_paths[0]
            item['image_path'] = os.path.join(os.path.abspath(self.store_path)
                                              ,image_path)  if image_path else ''
        return item






