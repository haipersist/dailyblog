#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'WHB'

import hashlib
import requests
import json

from .response import TextReply, MusicReply,ArticleReply
from .message import MSG_TYPES
from .utils import parse_xml
from .we_database import Database

class Wechat():

    def __init__(self):
        self.token = 'hbnnforever'
        self.secret ='1b2631e7e3a222abffb794916d162fb6'
        self.article_table = 'blog_wearticle'

    def auth(self,timestamp, nonce, signature,echostr):
        s = [timestamp, nonce, self.token]
        s.sort()
        s = ''.join(s)
        return echostr \
                if ( hashlib.sha1(s).hexdigest() == signature ) \
                else 'auth fail,plese retry'

    def get_access_token(self,secret):
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx2e10207d3d540b4a&secret=%s' % secret
        metadata = requests.get(url).content
        return json.loads(metadata)['access_token']

    def parse_data(self,metadata):
        data = parse_xml(metadata)
        self.msgtype = data.get('MsgType').lower()
        self.msg = MSG_TYPES.get(self.msgtype)(data)

    def resp_text(self,content):
        return TextReply(self.msg,content=content).render()

    def resp_voice(self,id):
        pass

    def resp_image(self,mediaid):
        pass

    def resp_music(self, title, desc, musicurl, hqurl):
       return MusicReply(self.msg,title=title,desc=desc,musicurl=musicurl,hqurl=hqurl).render()

    def response_video(self, media_id, title=None, description=None):
        pass

    def resp_article(self,articles):
        return ArticleReply(self.msg,articles).render()

    def get_all_from_db(self):
        we_db = Database('sae')
        data = we_db.get_all_titles(self.article_table)
        #data is a list whose item is a dict,the dict also contains id
        result = [(str(item['id']),item['title'],'\n') for item in data if item]
        if len(result)>10:
            return None
        return ' '.join(['.'.join(item) for item in result])

    def get_one_from_db(self,field):
        we_db = Database('sae')
        result = we_db.query_by_field(self.article_table, field)
        if result:
            result[0].setdefault('picurl','http://hbnnlove-hbnnlove.stor.sinaapp.com/large_Q39F_34d60001c9a8118f.jpg')
            result[0].pop('id')
        return result

    def insert_article(self,**kwargs):
        we_db = Database('sae')
        we_db.insert_by_dic(self.article_table,kwargs)

    def insert_data(self,tablename,**kwargs):
        db = Database('sae')
        db.insert_by_dic(tablename,kwargs)


    #send msg
    def send_text_msg(self,user,content):
        access_token = self.get_access_token(self.secret)
        return requests.post(
            url='https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s'%access_token,
            data={
                'touser': user,
                'msgtype': 'text',
                'text': {
                    'content': content,
                },
            }
        )





if __name__ == "__main__":
    chat = Wechat()
    xml = """
    <xml>
    <ToUserName><![CDATA[wechat]]></ToUserName>
    <FromUserName><![CDATA[pycharm]]></FromUserName>
    <CreateTime>dd</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[sss]]></Content>
    </xml>
    """
    title = 'dds'
    desc = 'dff'
    musicurl = 'f'
    hqurl = 'fg'
    chat.parse_data(xml)
    articles = [{'title':u'爱你','desc':u'记忆','picurl':'http://hbnn-hbnnstore.stor.sinaapp.com/boat.jpg',
                 'url':'http://finance.ifeng.com/a/20150630/13807969_0.shtml'},
                {'title':u'爱你','desc':u'记忆','picurl':'http://hbnn-hbnnstore.stor.sinaapp.com/europ.jpg',
                 'url':'http://finance.ifeng.com/a/20150630/13808481_0.shtml'}]
    #print chat.resp_article(articles)
