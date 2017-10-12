#encoding:utf-8

import os
import qrcode
from dailyblog.settings import SAE_APPKEY,SAE_SECRETKEY
import requests
from cStringIO import StringIO
from dailyblog.settings import DOMAIN,STATIC_ROOT


class PaperCode():

    """
    在SAE上不能进行文件读取，这是一个限制，无法正常将文件进行读写和存储
    """


    def __init__(self):
        self.baselink = DOMAIN
        self.curpath = os.path.abspath(os.path.dirname(__file__))


    def store_qrcode(self,article_alias):
        url = self.baselink + article_alias +'.html'
        #print url
        qrcode_file = os.path.join(STATIC_ROOT,'qrcode') + os.sep + article_alias +'.png'
        img = qrcode.make(url)
        img.save(qrcode_file)
        return '/static/qrcode/' + article_alias +'.png'


    def store_weixin_pic(self,url,pic_id):
        resp = requests.get(url)
        content = resp.content
        """
        self.bucket.put_object(pic_id+'.jpeg',content)
        return self.bucket.generate_url(pic_id+'.jpeg')
        """





if __name__ =="__main__":
    pc = PaperCode()
    pc.store_qrcode('wechat22')



