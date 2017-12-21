#encoding:utf-8

"""
As for every article,it needs generate one qrcode,which
is used to share it to wechat.

Papercode could convert one article url into one qrcode.


 :copyright: (c) 2017 by Haibo Wang.

"""



import os
import qrcode
import requests
from dailyblog.settings import DOMAIN,STATIC_ROOT




class PaperCode():

    """
    Convert the aritlce Paper code into one qrcode
    """


    def __init__(self):
        self.baselink = DOMAIN
        self.curpath = os.path.abspath(os.path.dirname(__file__))


    def store_qrcode(self,article_alias):
        url = self.baselink + '/article/' + article_alias +'.html'
        #the qrcode will be stored in static/qrcode/ temporally,it's not a good idea
        #because when the number of articles becomes bigger,it need bigger space.
        qrcode_file = os.path.join(STATIC_ROOT,'qrcode') + os.sep + article_alias +'.png'
        img = qrcode.make(url)
        img.save(qrcode_file)
        return '/static/qrcode/' + article_alias +'.png'






if __name__ =="__main__":
    pc = PaperCode()
    pc.store_qrcode('wechat22')



