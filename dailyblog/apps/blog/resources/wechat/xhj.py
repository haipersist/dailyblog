#-*-coding:utf-8 -*-
"""
it  provides a interface between wechat and tuling robot.
The tuling is very wonderful,it contains lots of convenient funcitons.
some things needed to be done:
1、sort them by api categories.
2、In wechat ,we should use it by different categories.

"""
import urllib2
import requests

class XHJ():

    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'Referer':'http://www.simsimi.com/',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0',
        }

    def resp(self,msg):
        msg = urllib2.quote(msg.encode('UTF-8'))
        self.apikey = '1b54d25299e544fd986918f2cce58e27'
        url = 'http://www.tuling123.com/openapi/api?info=%s&key=%s' % (msg,self.apikey)
        #print url
        resp = self.session.post(url,headers=self.headers).json()

        return (resp['text'],resp['url']) if resp.has_key('url') else resp['text']

if __name__ == "__main__":
    xhj = XHJ()
    print xhj.resp(u'北京天气')
    print xhj.session.cookies
    print xhj.resp(u'醋溜白菜')


